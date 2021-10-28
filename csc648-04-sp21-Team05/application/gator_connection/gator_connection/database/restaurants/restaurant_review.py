from gator_connection.models import *

from gator_connection.database.gator_connection_exceptions import *


class RestaurantReviews:
    """
    A class that helper for Restaurant's function implements.

    **Methods:**
    - postRestaurantReview(request, restaurant_id)
    - getAllRestaurantReviews(restaurant_id)

    """

    @staticmethod
    def postRestaurantReview(request, restaurant_id):
        """
        This is a function that help Restarant function implements (get data from form and post to database).
        :param request: Should be a POST HttpRequest object that contains values from the Request Restaurant Review
        :type request: HttpRequest
        :return: None
        :param restaurant_id: The requested restaurant to retrieve from the database
        :type restaurant_id: int
        :raises:ValidationError : If user is not logged in.
        :raises GatorConnectionError: If data from Restaurant tp post is invalid or missing
        :raises InvalidFormError: If data from Restaurant form is invalid or missing
        """
        # Get data from form
        title = request.POST.get('title')
        rating = request.POST.get('rating2')
        description = request.POST.get('description')

        # Check if user is logged in
        try:
            reg_user_id = request.session['reg_user_id']
            registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)
        except (AttributeError, KeyError, RegisteredUser.DoesNotExist):
            raise ValidationError("You must be logged in to post a restaurant review.")

        title_length = len(title)

        if title_length > 60:
            raise InvalidFormError(title, f"should be less than 60 characters. Current Length: {title_length}")

        # Get the restaurant from the database
        try:
            restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)
        except Restaurant.DoesNotExist:
            raise GatorConnectionError("Something went wrong when posting restaurant review. Please try again later.")

        # Create the new Restaurant Review Object
        restaurant_review = RestaurantReview()
        restaurant_review.restaurant = restaurant
        restaurant_review.title = title
        restaurant_review.description = description
        restaurant_review.rating = rating
        restaurant_review.registered_user = registered_user

        restaurant_review.save()

    @staticmethod
    def getAllRestaurantReviews(restaurant_id):
        """
        This is a function that help Restarant function implements (get data from database).

        :param restaurant_id: The requested restaurant to retrieve from the database
        :type restaurant_id: int
        :return: None or The restaurantReview from database
        :rtype: RestaurantReview
        """
        # Get the restaurant from the database
        try:
            restaurant = Restaurant.objects.get(restaurant_id=restaurant_id)

            return RestaurantReview.objects.filter(restaurant=restaurant)
        except Restaurant.DoesNotExist:
            return None
