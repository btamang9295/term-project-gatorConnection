# Import Django HttpRequest Object for documentation reasons
from django.http.request import HttpRequest

# Import Django Models Q for filtering database
from django.db.models import Q

# Import all Database ORM models created by Django
from gator_connection.models import *

# Import all custom Gator Connection Exceptions
from gator_connection.database.gator_connection_exceptions import *

# Import custom Address Validation class
from gator_connection.database.address import Address as AddressValidation

# Import Django Email to send email notifications
from django.core.mail import send_mail
from gator_connection.database.email_helper import EmailHelper

# Import custom HousingPost ORM for Full Text Search
from gator_connection.database.housing.housing_orm import HousingPost

from gator_connection.models import HousingListingRequest


class Housing:
    """
    A class that abstracts database interactions for Housing Listing Posts such as retrieving Housing Listing Posts,
    saving Housing Listing Posts, and searching Housing Listing Posts.

    **Methods:**
    - saveHousingFormInformation(request)
    - editHousingListing(request, housing_id)
    - deleteHousingListing(request, housing_id)
    - getHousingPosts(request)
    - getAllHousingPosts()
    - getHousingPost(housing_id)

    """

    @staticmethod
    def saveHousingFormInformation(request):
        """
        This function takes in a HttpRequest POST object. Extracts all of the necessary data to fill the fields in
        our Gator Connection database. Creates a Housing Listing Post Django ORM object and uses Django's built-in
        ORM features to save the object created from the information in the HttpRequest POST object into the database.

        :type request: HttpRequest
        :param request: Should be a POST HttpRequest object that contains values from the Request Housing Listing Form
        :return: None
        :raises GatorConnectionError: If data from Request Housing Listing Form is invalid or missing
        """
        try:
            requestData = Housing.__extractHousingPostRequestData(request)
        except GatorConnectionError as e:
            raise e

        image_post = request.FILES.get('image_path')

        address = Housing.__saveAddress(requestData.get('zipcode'), requestData.get('number'),
                                        requestData.get('street'), requestData.get('city'))

        post = Housing.__savePost(requestData.get('title'), requestData.get('description'),
                                  requestData.get('registered_user'))

        housing_listing_post = HousingListingPost()

        housing_listing_post.price = requestData.get('price')
        housing_listing_post.post = post
        housing_listing_post.are_pets_allowed = requestData.get('are_pets_allowed')
        housing_listing_post.preferred_pay_type = requestData.get('preferred_payment')
        housing_listing_post.address = address
        housing_listing_post.save()

        # send email to let owner know his housing website address.

        # code=housing_listing_post.item_id
        # email = request.session['email']
        # first_name = request.session['first_name']
        # EmailHelper.send_email(email, first_name,code, 2)

        Housing.__saveImage(post, image_post)

    @staticmethod
    def editHousingListing(request, housing_id):
        """
        This function takes in a HttpRequest POST object and the id of a housing listing. Extracts all of the necessary
        data in the request object to fill the fileds in our Gator Connection database. Queries the database for an
        existing Housing Listing Post using the *housing_id* using Django's built-in ORM. Then it uses the extracted
        data from the HttpRequest POST object and updates the values of the Housing Listing Post object. Then it
        saves the newly updated Housing Listing Post object into the database.

        :type request: HttpRequest
        :param request: Should be a POST HttpRequest object that contains values from the Edit Housing Listing Form
        :type housing_id: int
        :param housing_id: The ID of the Housing Listing in the database that you would like to edit.
        :return: None
        :raises GatorConnectionError: If data from Request Housing Listing Form is invalid or missing
        """
        try:
            requestData = Housing.__extractHousingPostRequestData(request)
        except GatorConnectionError as e:
            raise e

        # Get image if user added one
        try:
            image_post = request.Files.get('image_path')
        except AttributeError:
            image_post = None

        # Get the corresponding housing_listing_post
        try:
            housing_listing_post = HousingListingPost.objects.get(housing_id=housing_id)
        except HousingListingPost.DoesNotExist:
            raise GatorConnectionError("Something went wrong, this housing listing post no longer exists")

        # Edit Post model fields
        housing_listing_post.post.title = requestData.get('title')
        housing_listing_post.post.description = requestData.get('description')

        housing_listing_post.post.save()

        # Edit housing listing model fields
        housing_listing_post.price = requestData.get('price')
        housing_listing_post.are_pets_allowed = requestData.get('are_pets_allowed')
        housing_listing_post.preferred_pay_type = requestData.get('preferred_payment')

        # Edit address model fields
        housing_listing_post.address.zipcode = requestData.get('zipcode')
        housing_listing_post.address.number = requestData.get('number')
        housing_listing_post.address.street = requestData.get('street')
        housing_listing_post.address.city = requestData.get('city')

        housing_listing_post.address.save()

        housing_listing_post.save()

        # Create/Add new image
        Housing.__saveImage(housing_listing_post.post, image_post)

    @staticmethod
    def deleteHousingListing(request, housing_id):
        """
        This function takes in a HttpRequest POST object and the id of a housing listing. This function validates
        the user that requested to delete the housing listing post corresponding to *housing_id* using Django's
        Sessions middleware. If the user is authenticated and the one that posted the housing listing, this function
        queries the database for the housing listing post using the *housing_id*. Then it uses Django's ORM
        delete() function to delete the Housing Listing Post from the database.

        :type request: HttpRequest
        :param request: Should be a POST HttpRequest object
        :type housing_id: int
        :param housing_id: The ID of the housing listing in the database that has been requested to be deleted
        :return: None
        :raises GatorConnectionError: If user that made request is
        not authenticated, not the user that posted the housing listing or the housing listing post that was
        requested to be deleted doesn't exist
        """
        # Double check that the registered user is the one who posted
        try:
            reg_user_id = request.session['reg_user_id']
        except KeyError:
            raise GatorConnectionError("You are not validated. Please log out and log back in again and retry.")

        try:
            registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)
        except RegisteredUser.DoesNotExist:
            raise GatorConnectionError("You are not the owner of this post. You are forbidden from deleting this post")


        try:
            housing_listing = HousingListingPost.objects.get(housing_id=housing_id)

        except HousingListingPost.DoesNotExist:
            raise GatorConnectionError("Something went wrong. This post already does not exist.")

        housing_requests = HousingListingRequest.objects.filter(housing_listing=housing_listing)

        email = []

        for housing_request in housing_requests:
            try:
                housing_request_user = User.objects.get(user_id=housing_request.registered_user.user.user_id)


            except RegisteredUser.DoesNotExist:
                raise GatorConnectionError("Registered User that made housing request no longer exists.")

            try:
                account = Account.objects.get(user=housing_request_user)
                reg_user_email = Account.objects.get(user=registered_user.user)
            except Account.DoesNotExist:
                raise GatorConnectionError("Account that corresponds to Registered User no longer exists.")

            email.append(account.email)

        email_content = "The item you were interested: \n{}\nin has been closed by the owner.".format(housing_listing.post.title)

        # TODO: Add notification logic here as well
        # notification = Notification()
        #
        # notification.registered_user = housing_listing.post.registered_user
        # notification.message = f"{registered_user.first_name} {registered_user.last_name} is interested in your housing listing post."
        #
        # notification.save()


        send_mail(
            'Requested Housing Listing Has Been Closed',
            email_content,
            'Do Not Reply | Gator-connection',
            email,
            fail_silently=False
        )



        housing_listing.delete()

        # NOTE:
        #       This code is the start to pull each of the duplicate housing_listing id's.
        #       Then, it will allow us to pull each of the registered users associated to the id's
        #       and send them an email that the housing listing has been deleted.

        # housing_request = HousingListingRequest.objects.values('housing_listing').annotate(Count(''))




    @staticmethod
    def getHousingPosts(request):
        """
        This function takes in a HttpRequest GET object. This function extracts the query parameters from the request
        object if they exist. If the query parameters exist, this function calls *searchHousingPosts()*. If the query
        parameter does not exist, this function calls *getAllHousingPosts()*.

        :type request: HttpRequest
        :param request: Should be a GET HttpRequest object that has a search_query
        :return: An array of dictionaries with keys {"post", "housing", "images"}
        :rtype: list[dict]
        """
        search_query = request.GET.get('search')

        # No need to search
        if search_query is None or len(search_query) <= 0:
            return Housing.getAllHousingPosts()

        # Get search category to filter by
        search_category = request.GET.get('post_categories')

        return Housing.searchHousingPosts(search_query, search_category)

    @staticmethod
    def getAllHousingPosts():
        """
        This function is a helper function for *getHousingPosts()*. This function uses Django's ORM to get all rows in
        the Housing Listing Post table in our database. Because this table does not have all of the data needed for
        rendering on the frontend, for each row returned from the database, this function queries for the corresponding
        post and images. Then this function builds a dictionary to return to the frontend for easy access.

        :return: An array of dictionaries with keys {"post", "housing", "images"}
        :rtype: list[dict]
        """

        # Get all housing listing posts
        housing_listings = HousingListingPost.objects.all()

        template_data = []

        for housing_listing in housing_listings:
            post = Post.objects.get(post_id=housing_listing.post.post_id)
            try:
                images = Image.objects.filter(post=housing_listing.post.post_id)
            except Image.DoesNotExist:
                images = None

            template_data.append(
                {
                    "post": post,
                    "housing": housing_listing,
                    "images": images
                }
            )
        return template_data

    @staticmethod
    def getHousingPost(housing_id):
        """
        This function retrieves the housing listing post that corresponds to the *housing_id* given.

        :type housing_id: int
        :param housing_id: The requested housing listing post to retrieve from the database
        :return: A dictionary with keys {"post", "housing", "images"}
        :rtype: dict
        """
        try:
            housing_listing = HousingListingPost.objects.get(housing_id=housing_id)
        except HousingListingPost.DoesNotExist:
            raise GatorConnectionError("Sorry, this housing listing post does not exist anymore.")

        images = Image.objects.filter(post=housing_listing.post)

        template_data = []

        post = Post.objects.get(post_id=housing_listing.post.post_id)

        template_data = {
            "post": post,
            "housing": housing_listing,
            "images": images
        }

        return template_data

    @staticmethod
    def searchHousingPosts(search_query, search_category):
        """
        This function is a helper function for *getHousingPosts()*. Depending on the *search_category*, this function
        will use Django's ORM filter() to search for rows in our database. Or, this function will call our custom
        *Housing_ORM.search()* function that uses MySQL InnoDB's Full Text Search feature.

        :type search_query: str
        :param search_query:
        :type search_category: str
        :param search_category:
        :return: An array of dictionaries with keys {"post", "housing", "images"}
        :rtype: list[dict]
        """

        template_data = []

        # Full Text Search does not support data types that are not text/strings so use basic search functionality
        if search_category == 'pricing':
            housing_listings = HousingListingPost.objects.filter(
                Q(price__icontains=search_query) | Q(preferred_pay_type__icontains=search_query))
        elif search_category == 'preferred_payment':
            housing_listings = HousingListingPost.objects.filter(Q(preferred_pay_type__icontains=search_query))
        # Our Address table has many categories that are not compatible with Full Text Search, thus we will use a basic LIKE
        # search to give users more results
        elif search_category == 'location':
            housing_listings = HousingListingPost.objects.filter(Q(address__street__icontains=search_query) |
                                                                 Q(address__city__icontains=search_query) | Q(
                address__zipcode__icontains=search_query) |
                                                                 Q(address__city__icontains=search_query) | Q(
                address__number__icontains=search_query))
        else:
            # Full Text Search should be supported, so pass along the search_category
            return HousingPost.search(search_query, search_category)

        for housing_listing in housing_listings:
            post = Post.objects.get(post_id=housing_listing.post.post_id)
            try:
                images = Image.objects.filter(post=housing_listing.post)
            except Image.DoesNotExist:
                images = None

            template_data.append(
                {
                    "post": post,
                    "housing": housing_listing,
                    "images": images
                }
            )
        return template_data

    @staticmethod
    def getHousingPostsByUser(request):
        reg_user_id = request.session.get('reg_user_id')

        if not reg_user_id:
            raise GatorConnectionError("You are not authenticated.")

        # Get the Registered User object of the user
        try:
            registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)
        except RegisteredUser.DoesNotExist:
            raise GatorConnectionError("You must be logged in.")

        # Get all housing posts that the user posted
        housing_listings = HousingListingPost.objects.filter(post__registered_user=registered_user)

        template_data = []

        for housing_listing in housing_listings:
            post = Post.objects.get(post_id=housing_listing.post.post_id)
            try:
                images = Image.objects.filter(post=housing_listing.post)
            except Image.DoesNotExist:
                images = None

            template_data.append(
                {
                    "post": post,
                    "housing": housing_listing,
                    "images": images
                }
            )
        return template_data





    @staticmethod
    def __extractHousingPostRequestData(request):
        """
        This is a private helper method that extracts all of the form data from the HttpRequest POST object.
        :type request: HttpRequest
        :param request: Should be a POST HttpRequest object that contains values from the Post/Edit Housing Listing Form
        :return: A dictionary with keys {"registered_user", "title", "description", "price", "preferred_payment",
        "are_pets_allowed", "zipcode", "number", "street", "city"}
        :rtype: dict
        """
        # Check to make sure user is logged in
        try:
            reg_user_id = request.session['reg_user_id']
            registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)

        except (KeyError, RegisteredUser.DoesNotExist):

            raise ValidationError(message="You must be logged in to post a house listing")

        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        preferred_payment = request.POST.get('preferred_payment')
        are_pets_allowed = request.POST.get('pets_allowed')

        zipcode = request.POST.get('zipcode')
        number = request.POST.get('number')
        street = request.POST.get('street')
        city = request.POST.get('city')

        title_length = len(title)

        if title_length > 45:
            raise InvalidFormError(title, f"should be less than 45 characters. Current Length: {title_length}")

        try:
            price_double = float(price)
        except ValueError:
            raise InvalidFormError(price, "should be a decimal.")

        # Validate address fields
        try:
            AddressValidation.validateAddress(zipcode, number, street, city)
        except GatorConnectionError as e:
            raise e

        if price_double > 10000:
            raise InvalidFormError(price_double, "is too expensive. This website is for SFSU students, please enter a "
                                                 "more reasonable amount.")

        if are_pets_allowed == 'on':
            are_pets_allowed = 'Yes'
        else:
            are_pets_allowed = 'No'

        requestData = {
            "registered_user": registered_user,
            "title": title,
            "description": description,
            "price": price_double,
            "preferred_payment": preferred_payment,
            "are_pets_allowed": are_pets_allowed,
            "zipcode": zipcode,
            "number": number,
            "street": street,
            "city": city,
        }

        return requestData

    @staticmethod
    def __saveAddress(zipcode, number, street, city):
        """
        Helper method to save an Address into the database

        :param zipcode: Zipcode
        :param number: Street Number
        :param street: Street Name
        :param city: City Name
        :return: The Address object saved in the database
        :rtype: Address
        """

        # Create address
        address = Address()
        address.zipcode = zipcode
        address.number = number
        address.street = street
        address.city = city
        address.state = "CA"

        address.save()

        return address

    @staticmethod
    def __savePost(title, description, registered_user):
        """
        Helper method to save a Post into the database

        :type title: str
        :param title: The title of the post.
        :type description: str
        :param description: The description of the post.
        :type registered_user: RegisteredUser
        :param registered_user: The RegisteredUser object from the database that corresponds to the user that is
        requesting to save a Housing Listing Post into the database
        :return: The Post object saved in the database
        :rtype: Post
        """

        # Create post
        post = Post()

        post.title = title
        post.description = description
        post.registered_user = registered_user
        post.save()

        return post

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
