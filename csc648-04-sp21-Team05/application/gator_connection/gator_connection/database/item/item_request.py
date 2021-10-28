from gator_connection.models import *

from gator_connection.database.gator_connection_exceptions import *

from django.core.mail import send_mail


class ItemRequests:
    """
    A class that helper for Restaurant's function implements.

    **Methods:**
    - postItemRequest(request, item_id)
    - deleteItemRequest(request, item_id)
    - checkIfRequested(request, item_post)
    - getItemRequests(request)

    """
    @staticmethod
    def postItemRequest(request, item_id):
        """
        This is a function that help Item function implements (get data from form and post to database).

        :param request: Should be a POST HttpRequest object that contains values from the Item List Form
        :type request: HttpRequest
        :return: None
        :param item_id: The requested item to retrieve from the database
        :type item_id: int
        :raises:ValidationError : If user is not logged in.
        :raises GatorConnectionError: If data from Item tp post is invalid or missing
        """
        # Get all of the information from the item request form

        try:
            item_listing = ItemListingPost.objects.get(item_id=item_id)
        except ItemListingPost.DoesNotExist:
            raise GatorConnectionError("Something went wrong when sending the Item Request, please try again later.")

        try:
            reg_user_id = request.session['reg_user_id']
            registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)
        except (KeyError, RegisteredUser.DoesNotExist) as e:
            raise ValidationError("You must be logged in to send a item request.")

        # Create Item request object and save it in database
        item_request = ItemListingRequest()
        item_request.item_listing = item_listing
        item_request.registered_user = registered_user

        item_request.save()

        # Create Item List Form and save it in database
        item_form = ItemListingForm()
        item_form.registered_user = registered_user
        item_form.item_listing_request = item_request

        item_form.save()

        post_owner = item_listing.post.registered_user

        try:
            post_owner_account = Account.objects.get(user=post_owner.user)
            reg_user_email = Account.objects.get(user=registered_user.user)
        except Account.DoesNotExist:
            raise GatorConnectionError('Post Owner account does not exist')

        email_content = 'Dear user' + ',\n\nName: ' + registered_user.first_name + registered_user.last_name + 'is interested in your item listing' + '\n\nhim/her email is ' + reg_user_email.email + '\n\nBest,\n\nGator-Connection'
        email_content_interested = 'You have made a request for ' + post_owner.first_name + "'s item listing.  If the post owner feels that you are a good match, he/she will email you." + '\n\nBest,\n\nGator-Connection'

        # Create Item Request Notification and save it in database
        notification = Notification()

        notification.registered_user = item_listing.post.registered_user
        notification.message = f"{registered_user.first_name} {registered_user.last_name} is interested in your item listing."

        notification.save()

        item_notification = ItemRequestNotification()
        item_notification.notification = notification
        item_notification.item_listing_request = item_request

        item_notification.save()

        # Sends email to the user who posted the item listing after filling out the form
        send_mail(
            'Item Listing Interest!',
            email_content,
            'Do Not Reply | Gator-connection',
            [post_owner_account.email],
            fail_silently=False
        )

        # Sends email to the user who interested the item listing after filling out the form
        send_mail(
            'Item Listing Interest!',
            email_content_interested,
            'Do Not Reply | Gator-connection',
            [reg_user_email.email],
            fail_silently=False
        )

    @staticmethod
    def deleteItemRequest(request, item_id):
        """
        This is a function that help Item function implements (get data from form and post to database).

        :param request: Should be a POST HttpRequest object that contains values from the Item List Form
        :type request: HttpRequest
        :return: None
        :param item_id: The requested item to retrieve from the database
        :type item_id: int
        :raises GatorConnectionError: If  user have not authenticated ,or post is invalid or missing
        """
        # Check if user is authenticated
        try:
            reg_user_id = request.session['reg_user_id']
        except KeyError:
            raise GatorConnectionError(
                "There is an error, you are not authenticated. Please log out and log back in and retry.")

        # Get registered user object
        try:
            registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)
        except RegisteredUser.DoesNotExist:
            raise GatorConnectionError("There is an error, you are not authenticated.")

        # Get Item Listing Post object

        try:
            item_listing = ItemListingPost.objects.get(item_id=item_id)
        except ItemListingPost.DoesNotExist:
            raise GatorConnectionError(
                "Something went wrong while deleting request, this item listing post no longer exists.")

        # Get requests of item listing object and registered user
        try:
            item_request = ItemListingRequest.objects.get(registered_user=registered_user, item_listing=item_listing)
        except ItemListingRequest.DoesNotExist:
            raise GatorConnectionError("Error, your request already does not exist.")

        item_request.delete()

    @staticmethod
    def checkIfRequested(request, item_post):
        """
        This is a function that help Item function implements (check the situation of Requested for Item).

        :type request: HttpRequest
        :param request: The HttpRequest GET object that should contain the user identification data
        :return True or False: The result of boolean for situation of Requested
        :rtype: Boolean
        """
        try:
            reg_user_id = request.session['reg_user_id']
        except KeyError:
            return False

        # Check if registered user is not the one who posted
        if reg_user_id != item_post.post.registered_user.reg_user_id:
            # Check if registered user already sent a request
            try:
                registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)
                item_request = ItemListingRequest.objects.get(registered_user=registered_user, item_listing=item_post)
            except (RegisteredUser.DoesNotExist, ItemListingRequest.DoesNotExist):
                return False

            # Item Listing Request exists, therefore, user has requested already
            return True

        # Else, registered user is the one who posted, so user can't request his/her own post
        return False

    @staticmethod
    def getItemRequests(request):
        """
        This is a function that help Item function implements (get data Item data from database).

        :type request: HttpRequest
        :param request: The HttpRequest GET object that should contain the user identification data
        :raises GatorConnectionError: If  user have not authenticated.
        :return: An array of ItemListingRequest objects
        :rtype: list[ItemListingRequest]
        """
        # Check if user is authenticated
        try:
            reg_user_id = request.session['reg_user_id']
        except KeyError:
            raise GatorConnectionError(
                "There is an error, you are not authenticated. Please log out and log back in and retry.")

        # Get registered user object
        try:
            registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)
        except RegisteredUser.DoesNotExist:
            raise GatorConnectionError("There is an error, you are not authenticated.")

        template_data = []

        # Get item listing requests for the item listing posts that the registered user has posted
        item_requests = ItemListingRequest.objects.filter(item_listing__post__registered_user=registered_user)

        # For each item request get the email of the user that requested
        for item_request in item_requests:

            try:
                account = Account.objects.get(user=item_request.registered_user.user)
                email = account.email
            except Account.DoesNotExist:
                print("Registered user that requested does not have an account")
                email = None

            template_data.append({
                "item_request": item_request,
                "email": email,
            })

        return template_data
