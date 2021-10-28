from gator_connection.models import *
from django.db.models import Q

from gator_connection.database.gator_connection_exceptions import *
from gator_connection.database.item.item_orm import ItemPost

from gator_connection.database.email_helper import EmailHelper

from django.core.mail import send_mail

class Item:
    """
    A class that abstracts database interactions for Item Listing Posts such as retrieving Item Listing Posts,
    saving Item Listing Posts, and searching Item Listing Posts.

    **Methods:**
    - saveItemFormInformation(request)
    - editItemListing(request, item_id)
    - deleteItemListing(request, item_id)
    - getItemPosts(request)
    - getAllItemPosts()
    - getItemPost(item_id):
    - searchItemPosts(search_query, search_category)
    - getItemPostsByUser(request)
    """

    @staticmethod
    def saveItemFormInformation(request):
        """
        This function takes in a HttpRequest POST object. Extracts all of the necessary data to fill the fields in
        our Gator Connection database. Creates a Item Listing Post Django ORM object and uses Django's built-in
        ORM features to save the object created from the information in the HttpRequest POST object into the database.

        :type request: HttpRequest
        :param request: Should be a POST HttpRequest object that contains values from the Request Item Listing Form
        :return: None
        :raises GatorConnectionError: If data from Request Item Listing Form is invalid or missing
        """
        # Extract item form data from request object
        try:
            requestData = Item.__extractItemPostRequestData(request)
        except GatorConnectionError as e:
            raise e

        # Get image if user included one
        try:
            image_post = request.FILES.get('image_path')
        except AttributeError:
            image_post = None

        # Create Post object first and save in database because it will need to be used as foreign key
        post = Post()

        post.title = requestData.get('title')
        post.description = requestData.get('description')
        post.registered_user = requestData.get('registered_user')
        post.save()

        # Create Item Listing post and use Post object as foreign key
        item_listing_post = ItemListingPost()

        item_listing_post.price = requestData.get('price')
        item_listing_post.post = post
        item_listing_post.preferred_pay_type = requestData.get('preferred_payment')
        item_listing_post.condition = requestData.get('condition')
        item_listing_post.save()

        # send email to let owner know his item website address.

        # code=item_listing_post.item_id
        # email = request.session['email']
        # first_name = request.session['first_name']
        # EmailHelper.send_email(email, first_name,code,4)

        # If image was included, create Image object with Post object as foreign key
        Item.__saveImage(post, image_post)

    @staticmethod
    def editItemListing(request, item_id):
        """
        This function takes in a HttpRequest POST object and the id of a Item listing. Extracts all of the necessary
        data in the request object to fill the fileds in our Gator Connection database. Queries the database for an
        existing Item Listing Post using the *item_id* using Django's built-in ORM. Then it uses the extracted
        data from the HttpRequest POST object and updates the values of the Item Listing Post object. Then it
        saves the newly updated Item Listing Post object into the database.

        :type request: HttpRequest
        :param request: Should be a POST HttpRequest object that contains values from the Edit Item Listing Form
        :type item_id: int
        :param item_id: The ID of the Item Listing in the database that you would like to edit.
        :return: None
        :raises GatorConnectionError: If data from Request Item Listing Form is invalid or missing
        """
        try:
            requestData = Item.__extractItemPostRequestData(request)
        except GatorConnectionError as e:
            raise e

        try:
            image_post = request.FILES.get('image_path')
        except AttributeError:
            image_post = None

        # Get the corresponding item_listing_post
        try:
            item_listing_post = ItemListingPost.objects.get(item_id=item_id)
        except ItemListingPost.DoesNotExist:
            raise GatorConnectionError("Something went wrong, this item listing post no longer exists")

        # Edit Post model fields and save in database
        item_listing_post.post.title = requestData.get('title')
        item_listing_post.post.description = requestData.get('description')

        item_listing_post.post.save()

        # Edit Item Listing Model fields
        item_listing_post.price = requestData.get('price')
        item_listing_post.preferred_pay_type = requestData.get('preferred_payment')
        item_listing_post.condition = requestData.get('condition')

        item_listing_post.save()

        # Add new image if user provided it
        Item.__saveImage(item_listing_post.post, image_post)

    @staticmethod
    def deleteItemListing(request, item_id):
        """
        This function takes in a HttpRequest POST object and the id of a Item listing. This function validates
        the user that requested to delete the Item listing post corresponding to *item_id* using Django's
        Sessions middleware. If the user is authenticated and the one that posted the Item listing, this function
        queries the database for the Item listing post using the *item_id*. Then it uses Django's ORM
        delete() function to delete the Item Listing Post from the database.

        :type request: HttpRequest
        :param request: Should be a POST HttpRequest object
        :type item_id: int
        :param item_id: The ID of the Item listing in the database that has been requested to be deleted
        :return: None
        :raises GatorConnectionError: If user that made request is
        not authenticated, not the user that posted the Item listing or the Item listing post that was
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
            item_listing = ItemListingPost.objects.get(item_id=item_id)
        except ItemListingPost.DoesNotExist:
            raise GatorConnectionError("Something went wrong. This post already does not exist.")

        item_requests = ItemListingRequest.objects.filter(item_listing=item_listing)

        email = []

        for item_requests in item_requests:
            try:
                item_requests_user = User.objects.get(user_id=item_requests.registered_user.user.user_id)


            except RegisteredUser.DoesNotExist:
                raise GatorConnectionError("Registered User that made item request no longer exists.")

            try:
                account = Account.objects.get(user=item_requests_user)
            except Account.DoesNotExist:
                raise GatorConnectionError("Account that corresponds to Registered User no longer exists.")

            email.append(account.email)


        email_content = "The item you were interested: \n{}\nin has been closed by the owner.".format(item_listing.post.title)

        # TODO: Add notification logic here as well
        # notification = Notification()
        #
        # notification.registered_user = item_listing.post.registered_user
        # notification.message = f"{registered_user.first_name} {registered_user.last_name} is interested in your item listing post."
        #
        # notification.save()


        send_mail(
            'Requested Item Listing Has Been Closed',
            email_content,
            'Do Not Reply | Gator-connection',
            email,
            fail_silently=False
        )

        item_listing.delete()

    @staticmethod
    def __extractItemPostRequestData(request):
        """
        This is a private helper method that extracts all of the form data from the HttpRequest POST object.
        :type request: HttpRequest
        :param request: Should be a POST HttpRequest object that contains values from the Post/Edit Item Listing Form
        :return: A dictionary with keys {"registered_user", "title", "description", "price", "preferred_payment",
        "condition"}
        :rtype: dict
        """
        # Check to make sure user is logged in
        try:
            reg_user_id = request.session['reg_user_id']
            registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)

        except (KeyError, RegisteredUser.DoesNotExist):

            raise ValidationError(message="You must be logged in to post a item listing")

        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        preferred_payment = request.POST.get('preferred_payment')

        if request.POST.get('condition_good') == 'on':
            condition = 'Good'
        else:
            condition = 'Used'

        title_length = len(title)

        if title_length > 45:
            raise InvalidFormError(title, f"should be less than 45 characters. Current Length: {title_length}")

        try:
            price_double = float(price)
        except ValueError:
            raise InvalidFormError(price, "should be a decimal.")

        if price_double > 10000:
            raise InvalidFormError(price_double, "is too expensive. This website is for SFSU students, please enter a "
                                                 "more reasonable amount.")

        requestData = {
            "registered_user": registered_user,
            "title": title,
            "description": description,
            "price": price_double,
            "preferred_payment": preferred_payment,
            "condition": condition
        }

        return requestData

    @staticmethod
    def getItemPosts(request):
        """
        This function takes in a HttpRequest GET object. This function extracts the query parameters from the request
        object if they exist. If the query parameters exist, this function calls *searchItemPosts()*. If the query
        parameter does not exist, this function calls *getAllItemPosts()*.

        :type request: HttpRequest
        :param request: Should be a GET HttpRequest object that has a search_query
        :return: An array of dictionaries with keys {"post", "item", "images"}
        :rtype: list[dict]
        """
        search_query = request.GET.get('search')
        search_category = request.GET.get('post_categories')

        if search_query is None or len(search_query) <= 0:
            return Item.getAllItemPosts()

        return Item.searchItemPosts(search_query, search_category)

    @staticmethod
    def getAllItemPosts():
        """
        This function is a helper function for *getItemPosts()*. This function uses Django's ORM to get all rows in
        the Item Listing Post table in our database. Because this table does not have all of the data needed for
        rendering on the frontend, for each row returned from the database, this function queries for the corresponding
        post and images. Then this function builds a dictionary to return to the frontend for easy access.

        :return: An array of dictionaries with keys {"post", "item", "images"}
        :rtype: list[dict]
        """

        # Get all Item listing posts
        item_posts = ItemListingPost.objects.all()

        template_data = []

        for item_post in item_posts:
            post = Post.objects.get(post_id=item_post.post.post_id)
            try:
                images = Image.objects.filter(post=item_post.post.post_id)
            except Image.DoesNotExist:
                images = None

            template_data.append(
                {
                    "post": post,
                    "item": item_post,
                    "images": images
                }
            )
        return template_data

    @staticmethod
    def getItemPost(item_id):
        """
        This function retrieves the Item listing post that corresponds to the *item_id* given.

        :type item_id: int
        :param item_id: The requested Item listing post to retrieve from the database
        :return: A dictionary with keys {"post", "item", "images"}
        :rtype: dict
        """
        try:
            item_listing = ItemListingPost.objects.get(item_id=item_id)
        except ItemListingPost.DoesNotExist:
            raise GatorConnectionError("Sorry, this item listing post does not exist anymore.")

        images = Image.objects.filter(post=item_listing.post)

        post = Post.objects.get(post_id=item_listing.post.post_id)

        template_data = {
            "post": post,
            "item": item_listing,
            "images": images,
        }

        return template_data

    @staticmethod
    def searchItemPosts(search_query, search_category):
        """
        This function is a helper function for *getItemPosts()*. Depending on the *search_category*, this function
        will use Django's ORM filter() to search for rows in our database. Or, this function will call our custom
        *Item_ORM.search()* function that uses MySQL InnoDB's Full Text Search feature.

        :type search_query: str
        :param search_query:
        :type search_category: str
        :param search_category:
        :return: An array of dictionaries with keys {"post", "item", "images"}
        :rtype: list[dict]
        """

        if search_category == 'price':
            item_posts = ItemListingPost.objects.filter(
                Q(price__icontains=search_query) | Q(preferred_pay_type__icontains=search_query))
        elif search_category == 'preferred_payment':
            item_posts = ItemListingPost.objects.filter(Q(preferred_pay_type__icontains=search_query))
        else:
            return ItemPost.search(search_query, search_category)

        template_data = []

        for item_post in item_posts:
            post = Post.objects.get(post_id=item_post.post.post_id)
            try:
                images = Image.objects.filter(post=item_post.post)
            except Image.DoesNotExist:
                images = None

            template_data.append(
                {
                    "post": post,
                    "item": item_post,
                    "images": images,
                }
            )

        return template_data

    @staticmethod
    def getItemPostsByUser(request):
        """
        This function takes in a HttpRequest to select the item that own the logged user
        from database.

        :type request: HttpRequest
        :param request: Should be a GET HttpRequest object that has a search_query
        :return: An array of dictionaries with keys {"post", "item", "images"}
        :rtype: list[dict]
        """
        reg_user_id = request.session.get('reg_user_id')

        if not reg_user_id:
            raise GatorConnectionError("You are not authenticated.")

        # Get the Registered User object of the user
        try:
            registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)
        except RegisteredUser.DoesNotExist:
            raise GatorConnectionError("You must be logged in.")

        # Get all item posts that the user posted
        item_listings = ItemListingPost.objects.filter(post__registered_user=registered_user)

        template_data = []

        for item_listing in item_listings:
            post = Post.objects.get(post_id=item_listing.post.post_id)
            try:
                images = Image.objects.filter(post=item_listing.post)
            except Image.DoesNotExist:
                images = None

            template_data.append(
                {
                    "post": post,
                    "item": item_listing,
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
