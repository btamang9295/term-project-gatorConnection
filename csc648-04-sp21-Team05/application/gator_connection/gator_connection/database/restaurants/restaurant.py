from gator_connection.models import *
from django.db.models import Q, Avg

from gator_connection.database.gator_connection_exceptions import *

from gator_connection.database.address import Address as AddressValidation
from gator_connection.database.restaurants.restaurant_orm import RestaurantOrm as RestaurantORM


class Restaurants:
    """
    A class that abstracts database interactions for Restaurant such as retrieving Restaurant
    and Restaurant review, saving Restaurant and Restaurant review, and searching Restaurant.

    **Methods:**
    - postRestaurant(restaurant_request)
    - getRestaurants(request)
    - getRestaurant(restaurant_id)
    - searchRestaurants(search_query, search_category)
    - getReviews(restaurant)
    - getRestaurantRating(restaurant)
    - postImage(request, restaurant_id)

    """

    @staticmethod
    def postRestaurant(restaurant_request):
        """
        This function takes in a HttpRequest POST object. Extracts all of the necessary data to fill the fields in
        our Gator Connection database. Creates a Restaurant Django ORM object and uses Django's built-in
        ORM features to save the object created from the information in the HttpRequest POST object into the database.

        :type request: HttpRequest
        :param request: Should be a POST HttpRequest object that contains values from the Request Restaurant
        :return: None
        :raises GatorConnectionError: If data from Restaurant is invalid or missing
        """
        assert (isinstance(restaurant_request, RestaurantRequest))


        # Create the Restaurant object and save it in database
        restaurant = Restaurant()
        restaurant.name = restaurant_request.name
        restaurant.address = restaurant_request.address
        restaurant.description = restaurant_request.post.description
        restaurant.open = restaurant_request.open
        restaurant.close = restaurant_request.close
        restaurant.takeout = restaurant_request.takeout

        restaurant.save()

        images = Image.objects.filter(post=restaurant_request.post)

        # Create the Restaurant Image object and save it in database
        for image in images:
            restaurant_image = RestaurantImage()
            restaurant_image.image_path = image.image_path
            restaurant_image.restaurant = restaurant

            restaurant_image.save()




        # Delete post when save is successful
        restaurant_request.post.delete()

    @staticmethod
    def getRestaurants(request):
        """
        This function takes in a HttpRequest GET object. This function extracts the query parameters from the request
        object if they exist. If the query parameters exist, this function calls *searchRestaurants()*. If the query
        parameter does not exist, this function calls *getAllRestaurants()*.

        :param request: Should be a GET HttpRequest object that has a search_query
        :type request: HttpRequest
        :return: An array of dictionaries with keys {"restaurant", "rating", "images"} or {"address","restaurant", "rating", "images"} 
        :rtype: list[dict]
        """
        search_query = request.GET.get('search')

        if search_query is None or len(search_query) <= 0:
            return Restaurants.getAllRestaurants()

        search_category = request.GET.get('post_categories')

        return Restaurants.searchRestaurants(search_query, search_category)

    @staticmethod
    def getAllRestaurants():
        """
        This function is a helper function for *getAllRestaurants()*. This function uses Django's ORM to get all rows in
        the Restaurant table in our database. Because this table does not have all of the data needed for
        rendering on the frontend, for each row returned from the database, this function queries for the corresponding
        post and images. Then this function builds a dictionary to return to the frontend for easy access.

        :return: An array of dictionaries with keys {"address","restaurant", "rating", "images"}
        :rtype: list[dict]
        """
        # Get all restaurants
        restaurants = Restaurant.objects.all()

        template_data = []

        for restaurant in restaurants:
            address = Address.objects.get(address_id=restaurant.address.address_id)

            try:
                images = RestaurantImage.objects.filter(restaurant=restaurant)
            except RestaurantImage.DoesNotExist:
                images = None

            rating = Restaurants.getRestaurantRating(restaurant)

            template_data.append(
                {
                    "address": address,
                    "restaurant": restaurant,
                    "rating": rating,
                    "images": images
                }
            )

        return template_data

    @staticmethod
    def getRestaurant(restaurant_id):
        """
        This function retrieves the Restaurant that corresponds to the *restaurant_id* given.

        :type restaurant_id: int
        :param restaurant_id: The requested restaurant to retrieve from the database
        :return: A dictionary with keys {"address","restaurant", "rating", "images"} 
                                    or  {"address","restaurant", "rating", "images","related_restaurants","reviews"}
        :rtype: dict
        """
        try:
            restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise GatorConnectionError("Something went wrong. Could not find restaurant. Please try again later.")


        address = Address.objects.get(address_id=restaurant.address.address_id)

        try:
            images = RestaurantImage.objects.filter(restaurant=restaurant)
        except RestaurantImage.DoesNotExist:
            images = None

        rating = Restaurants.getRestaurantRating(restaurant)

        # Get all of the other restaurants
        related_restaurants = Restaurant.objects.exclude(restaurant_id=restaurant_id)

        data = []

        for related_restaurant in related_restaurants:
            related_address = Address.objects.get(address_id=related_restaurant.address.address_id)

            try:
                related_images = RestaurantImage.objects.filter(restaurant=related_restaurant)
            except RestaurantImage.DoesNotExist:
                related_images = None

            related_rating = Restaurants.getRestaurantRating(related_restaurant)

            data.append(
                {
                    "address": related_address,
                    "restaurant": related_restaurant,
                    "rating": related_rating,
                    "images": related_images
                }
            )

        reviews = Restaurants.getReviews(restaurant)

        return {
            'address': address,
            'restaurant': restaurant,
            'rating': rating if rating is not None else 0,
            'images': images,
            'related_restaurants': data,
            'reviews': reviews,
        }

    @staticmethod
    def searchRestaurants(search_query, search_category):
        """
        This function is a helper function for *getRestaurant()*. Depending on the *search_category*, this function
        will use Django's ORM filter() to search for rows in our database. Or, this function will call our custom
        *Restaurant_ORM.search()* function that uses MySQL InnoDB's Full Text Search feature.

        :type search_query: str
        :param search_query: Should be a GET HttpRequest object that has a search_query
        :type search_category: str
        :param search_category: Should be a GET HttpRequest object that has a search_category
        :return: An array of dictionaries with keys {"restaurant", "rating", "images"}
        :rtype: list[dict]
        """
        if search_category == 'location':
            restaurants = Restaurant.objects.filter(Q(address__street__icontains=search_query) |
                                                    Q(address__city__icontains=search_query) | Q(
                address__zipcode__icontains=search_query) |
                                                    Q(address__city__icontains=search_query) | Q(
                address__number__icontains=search_query))
        else:
            template_data = RestaurantORM.search(search_query, search_category)

            for restaurant_data in template_data:
                # Need to get the rating of each restaurant
                restaurant_data['rating'] = Restaurants.getRestaurantRating(restaurant_data.get('restaurant'))

            return template_data

        template_data = []

        for restaurant in restaurants:
            try:
                images = RestaurantImage.objects.filter(restaurant=restaurant)
            except RestaurantImage.DoesNotExist:
                images = None

            rating = Restaurants.getRestaurantRating(restaurant)

            template_data.append(
                {
                    "restaurant": restaurant,
                    "rating": rating,
                    "images": images
                }
            )

        return template_data

    @staticmethod
    def getReviews(restaurant):
        """
        This function is a helper function for *getRestaurants()*. This function uses Django's ORM to get all rows in
        the Restaurant table in our database. Because this table does not have all of the data needed for
        rendering on the frontend, for each row returned from the database, this function queries for the corresponding
        post. Then this function builds a dictionary to return to the frontend for easy access.

        :return: An array of dictionaries with keys {"review"}
        :rtype: list[dict]
        """
        data = []
        reviews = RestaurantReview.objects.filter(restaurant=restaurant)

        for review in reviews:
            data.append({
                "review": review,
            })
        return data

    @staticmethod
    def getRestaurantRating(restaurant):
        """
        This function is a helper function for *getAllRestaurants()*,*getRestaurants()*,*searchRestaurants()*.
        This function uses Django's ORM to get all rows in the Restaurant table in our database. Because 
        this table does not have all of the data needed for rendering on the frontend, for each row returned 
        from the database, this function queries for the correspondingpost and images. Then this function builds
         a dictionary to return to the frontend for easy access.

        :return: An array of dictionaries with keys {"revie"}
        :rtype: list[dict]
        """
        # Get all of the restaurant reviews associated with the restaurant
        rating = RestaurantReview.objects.filter(restaurant=restaurant).aggregate(Avg('rating'))

        return rating

    @staticmethod
    def postImage(request, restaurant_id):
        """
        Helper Method to save an image into the database

        :type request: Post
        :param posrequestt: The Post object that is already saved in the database that this image will belong to
        :type restaurant_id: int
        :param restaurant_id: The requested restaurant to retrieve from the database
        :raises:ValidationError : If user is not logged in.
        :raises:GatorConnectionError : If data from Restaurant to Post is invalid or missing
        :return: The Image object saved in the database
        :rtype: Image
        """
        # Check if user is logged in
        try:
            reg_user_id = request.session['reg_user_id']
            registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)
        except (AttributeError, KeyError, RegisteredUser.DoesNotExist):
            raise ValidationError("You must be logged in to post a restaurant review.")

        try:
            restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise GatorConnectionError("Something went wrong while posting image. Please try again later.")

        image_post = request.FILES.get('image')

        image = RestaurantImage()

        image.restaurant = restaurant
        image.image_path = image_post

        image.save()
