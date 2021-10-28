from gator_connection.models import *

from gator_connection.database.gator_connection_exceptions import *
from gator_connection.database.address import Address as AddressValidation


class RestaurantRequests:
    """
    A class that helper for Restaurant's function implements.

    **Methods:**
    - postRestaurantRequest(request)
    - getAllRequests():

    """
    @staticmethod
    def postRestaurantRequest(request):
        """
        This is a function that help restarant.py function implements.

        :type request: HttpRequest
        :param request: Should be a POST HttpRequest object that contains values from the Request Restaurant
        :return: None
        :raises GatorConnectionError: If data from Restaurant is invalid or missing
        """
        # Get all restaurant request information from request
        name = request.POST.get('name')
        description = request.POST.get('description')

        zipcode = request.POST.get('zipcode')
        street = request.POST.get('street')
        number = request.POST.get('number')
        city = request.POST.get('city')
        open_time = request.POST.get('open-time')
        close_time = request.POST.get('close-time')
        takeout = request.POST.get('takeout')

        # Check to make sure user is logged in
        try:
            reg_user_id = request.session['reg_user_id']
            registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)

        except (KeyError, RegisteredUser.DoesNotExist):

            raise ValidationError(message="You must be logged in to make a request to add a restaurant.")

        try:
            # Check if address is valid
            AddressValidation.validateAddress(zipcode, number, street, city)
        except GatorConnectionError as e:
            raise e

        name_length = len(name)

        if name_length > 45:
            raise InvalidFormError(name, f"should be less than 45 characters. Current length: {name_length}")

        if takeout == 'on':
            takeout = 'Yes'
        else:
            takeout = 'No'

        try:
            image_post = request.FILES.get('image_path')
        except AttributeError:
            image_post = None

        # Create Address object and save it in database
        address = Address()
        address.zipcode = zipcode
        address.street = street
        address.number = number
        address.city = city
        address.state = "CA"

        address.save()

        # Create Post
        post = Post()
        post.title = name
        post.description = description
        post.registered_user = registered_user

        post.save()

        # Create Restaurant Request Object and save it in database
        restaurant_request = RestaurantRequest()
        restaurant_request.name = name
        restaurant_request.address = address
        restaurant_request.open = open_time
        restaurant_request.close = close_time
        restaurant_request.post = post
        restaurant_request.takeout = takeout
        restaurant_request.save()

        # Create image
        RestaurantRequests.__saveImage(post, image_post)

    @staticmethod
    def getAllRequests():
        """
        This is a function that help Restarant function implements (get the data from databse).

        :return: An array of dictionaries with keys {"post","restaurant_request", "images"}
        :rtype: list[dict]
        """
        restaurant_requests = RestaurantRequest.objects.all()

        template_data = []

        for restaurant_request in restaurant_requests:
            post = Post.objects.get(post_id=restaurant_request.post.post_id)
            try:
                images = Image.objects.filter(post=restaurant_request.post.post_id)
            except Image.DoesNotExist:
                images = None

            template_data.append(
                {
                    "post": post,
                    "restaurant_request": restaurant_request,
                    "images": images
                }
            )
        return template_data

    @staticmethod
    def __saveImage(post, image_post):
        """
        Helper Method to save an image into the database

        :type post: Post
        :param post: The Post object that is already saved in the database that this image will belong to
        :type image_post: HttpRequest.FILES
        :param image_post: The image file that was inputted by the user
        :return: The Image object saved in the database
        :rtype: Image
        """
        if not (image_post is None):
            image = Image()

            image.image_path = image_post
            image.post = post
            image.save()
