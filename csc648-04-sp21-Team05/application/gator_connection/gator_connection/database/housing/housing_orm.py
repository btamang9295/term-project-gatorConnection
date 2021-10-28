from gator_connection.database.database import Database
from gator_connection.database.sql_builder import SQLBuilder
from gator_connection.database.search import Search
from gator_connection.database.gator_connection_exceptions import *

from gator_connection.models import Post, Address, Image


class HousingPost:
    """
    A class that helper for Housing's function implements.

    **Methods:**
    - search(search_query, search_category)

    """
    table_name = "`Housing Listing Post`"

    @staticmethod
    def search(search_query, search_category):
        """
        This is a function that help housing.py search function implements (get the data from databse).

        :param search_query: Should be a GET HttpRequest object that has a search_query
        :type search_query: str
        :param search_category: Should be a GET HttpRequest object that has a search_category
        :type search_category: str
        :return: An array of dictionaries with keys {"post", "housing", "images"}
        :rtype: list[dict]
        """
        # Search Database using MySQL's Full Text Search

        sql = SQLBuilder()

        if search_category == 'title':
            sql.select('* FROM {} AS {}', [HousingPost.table_name, 'housing']).raw_sql(' JOIN {} AS {} ON {} = {}',
                                                                                       ["Post", "post", "post.post_id",
                                                                                        "housing.post"]) \
                .where('').match(['post.title']).against('\'{}\' IN BOOLEAN MODE', [
                Search.format_query_string(search_query)])
        else:
            sql.select('* FROM {} AS {}', [HousingPost.table_name, 'housing']).raw_sql(' JOIN {} AS {} ON {} = {}',
                                                                                       ["Post", "post", "post.post_id",
                                                                                        "housing.post"]) \
                .where('').match(['housing.are_pets_allowed', 'housing.preferred_pay_type']).against(
                '\'{}\' IN BOOLEAN MODE', [Search.format_query_string(search_query)]) \
                .raw_sql(' OR').match(['post.title', 'post.description']).against('\'{}\' IN BOOLEAN MODE', [
                Search.format_query_string(search_query)])

        # Run SQL query in Database
        results = Database.selectQuery(str(sql))

        template_data = []

        # For each row returned in results, create a HousingPost object, get Post object, and get Address object
        # Then append this as a dictionary to the housing array similarly to how the getAllHousingPosts returns
        # data
        for result in results:

            # Create HousingPost object
            housing = HousingPost()
            housing.housing_id = result.get('housing_id')
            housing.price = result.get('price')
            housing.are_pets_allowed = result.get('are_pets_allowed')
            housing.post = result.get('post_id')
            housing.preferred_pay_type = result.get('preferred_pay_type')
            housing.address = result.get('address')

            # Get the Post object and Address object using Django's ORM
            try:
                post = Post.objects.get(post_id=housing.post)
                address = Address.objects.get(address_id=housing.address)
            except (Post.DoesNotExist, Address.DoesNotExist):
                raise GatorConnectionError("Could not find corresponding post object for housing listing")

            # Get the images associated with the Post object
            try:
                images = Image.objects.filter(post=post)
            except Image.DoesNotExist:
                images = None

            # Set housing.address to Address object to match how getAllHousingPosts returns data
            housing.address = address

            template_data.append(
                {
                    "post": post,
                    "housing": housing,
                    "images": images
                }
            )

        return template_data

    def __init__(self):
        self.housing_id = None
        self.price = None
        self.are_pets_allowed = None
        self.post = None
        self.preferred_pay_type = None
        self.address = None
