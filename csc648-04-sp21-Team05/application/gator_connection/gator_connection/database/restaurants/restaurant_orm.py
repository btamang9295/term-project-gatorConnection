from gator_connection.database.database import Database
from gator_connection.database.sql_builder import SQLBuilder
from gator_connection.database.search import Search
from gator_connection.database.gator_connection_exceptions import *
from gator_connection.models import Address, Restaurant, RestaurantImage


class RestaurantOrm:
    """
    A class that helper for Restaurant's function implements.

    **Methods:**
    - search(search_query, search_category)

    """
    table_name = "Restaurant"

    def __init__(self):
        self.restaurant_id = None
        self.name = None
        self.address = None
        self.post = None
        self.open = None
        self.close = None
        self.takeout = None

    @staticmethod
    def search(search_query, search_category):
        """
        This is a function that help restarant.py search function implements (get the data from databse).

        :param search_query: Should be a GET HttpRequest object that has a search_query
        :type search_query: str
        :param search_category: Should be a GET HttpRequest object that has a search_category
        :type search_category: str
        :return: An array of dictionaries with keys {"post", "restaurant", "images"}
        :rtype: list[dict]
        """
        sql = SQLBuilder()

        if search_category == 'name':
            sql.select('* FROM {} AS {}', [RestaurantOrm.table_name, 'restaurant'])\
                .where('').match(['restaurant.name']).against(
                '\'{}\' IN BOOLEAN MODE', [Search.format_query_string(search_query)])
        else:
            sql.select('* FROM {} AS {}', [RestaurantOrm.table_name, 'restaurant'])\
                .where('').match(['restaurant.name', 'restaurant.takeout', 'restaurant.description']).against(
                '\'{}\' IN BOOLEAN MODE', [Search.format_query_string(search_query)])

        results = Database.selectQuery(str(sql))

        template_data = []

        for result in results:
            # Create Restaurant object
            restaurant_orm = RestaurantOrm()
            restaurant_orm.restaurant_id = result.get('restaurant_id')
            restaurant_orm.name = result.get('name')
            restaurant_orm.address = result.get('address')
            restaurant_orm.open = result.get('open')
            restaurant_orm.close = result.get('close')
            restaurant_orm.takeout = result.get('takeout')

            # Get the Restaurant object and Address object using Django's ORM
            try:
                restaurant = Restaurant.objects.get(restaurant_id=restaurant_orm.restaurant_id)
            except Restaurant.DoesNotExist:
                continue

            try:
                address = Address.objects.get(address_id=restaurant_orm.address)
            except Address.DoesNotExist:
                raise GatorConnectionError("Could not find corresponding post/address object for restaurant")


            # Get the images associated with the Restaurant object
            try:
                images = RestaurantImage.objects.filter(restaurant=restaurant)
            except RestaurantImage.DoesNotExist:
                images = None


            template_data.append(
                {
                    "restaurant": restaurant,
                    "images": images
                }
            )
        return template_data
