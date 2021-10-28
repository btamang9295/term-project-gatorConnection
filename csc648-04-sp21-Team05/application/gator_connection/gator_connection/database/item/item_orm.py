from gator_connection.database.database import Database
from gator_connection.database.sql_builder import SQLBuilder
from gator_connection.database.search import Search
from gator_connection.database.gator_connection_exceptions import *

from gator_connection.models import Post, Image


class ItemPost:
    """
    A class that helper for Item's function implements.

    **Methods:**
    - search(search_query, search_category)

    """
    table_name = "`Item Listing Post`"

    def __init__(self):
        self.item_id = None
        self.price = None
        self.post = None
        self.preferred_pay_type = None

    @staticmethod
    def search(search_query, search_category):
        """
        This is a function that help Item.py search function implements (get the data from databse).

        :param search_query: Should be a GET HttpRequest object that has a search_query
        :type search_query: str
        :param search_category: Should be a GET HttpRequest object that has a search_category
        :type search_category: str
        :return: An array of dictionaries with keys {"post", "item", "images"}
        :rtype: list[dict]
        """
        sql = SQLBuilder()

        if search_category == 'title':
            sql.select('* FROM {} AS {}', [ItemPost.table_name, 'item']).raw_sql(' JOIN {} AS {} ON {} = {}',
                                                                                 ["Post", "post", "post.post_id",
                                                                                  "item.post"]) \
                .where('').match(['post.title']).against('\'{}\' IN BOOLEAN MODE', [
                Search.format_query_string(search_query)])
        else:
            sql.select('* FROM {} AS {}', [ItemPost.table_name, 'item']).raw_sql(' JOIN {} AS {} ON {} = {}',
                                                                                 ["Post", "post", "post.post_id",
                                                                                  "item.post"]) \
                .where('').match(['item.preferred_pay_type']).against(
                '\'{}\' IN BOOLEAN MODE', [Search.format_query_string(search_query)]) \
                .raw_sql(' OR').match(['post.title', 'post.description']).against('\'{}\' IN BOOLEAN MODE', [
                Search.format_query_string(search_query)])

        # Run SQL query in Database and return data in a dictionary
        results = Database.selectQuery(str(sql))

        template_data = []

        # For each row returned in results, create an ItemPost object
        # Get the Post object and Image objects using Django's ORM
        # Append to template_data as a dictionary to match how the front
        # end templates render data
        for result in results:
            # Create ItemPost object
            item = ItemPost()
            item.item_id = result.get('item_id')
            item.price = result.get('price')
            item.post = result.get('post_id')
            item.preferred_pay_type = result.get('preferred_pay_type')

            # Get the Post and Image objects using Django's ORM
            try:
                post = Post.objects.get(post_id=item.post)
            except Post.DoesNotExist:
                raise GatorConnectionError("Could not find corresponding post object for item listing")

            try:
                images = Image.objects.filter(post=post)
            except Image.DoesNotExist:
                images = None

            template_data.append(
                {
                    "post": post,
                    "item": item,
                    "images": images
                }
            )
        return template_data
