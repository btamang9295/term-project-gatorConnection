from gator_connection.models import *

from gator_connection.database.gator_connection_exceptions import *
from datetime import datetime

# Import Django HttpRequest Object for documentation reasons
from django.http.request import HttpRequest
from django.utils.timezone import make_aware
from django.core.mail import send_mail

import re


class HousingRequests:
    """
    A class that helper for Housing's function implements.

    **Methods:**
    - postHousingRequest(request, housing_id)
    - deleteHousingRequest(request, housing_id)
    - checkIfRequested(request, housing_post)
    - housingFormNotification(request, housing_post)
    - getHousingRequests(request)
    """
    @staticmethod
    def postHousingRequest(request, housing_id):
        # Get all of the information from the housing request form
        try:
            move_in_date = datetime.strptime(request.POST.get('graduation_date'), "%Y-%m-%d")

            if move_in_date.date() < datetime.now().date():
                raise GatorConnectionError("Cannot go back in time. Please enter a valid future date.")

            move_in_date = make_aware(move_in_date)
        except ValueError:
            raise GatorConnectionError("Date Format is incorrect, must be YYYY-MM-DD.")


        about_me = request.POST.get('about_me')

        phone_number = request.POST.get('phone_number')

        phone_number_format = '^[1-9]\d{2}-\d{3}-\d{4}'

        if len(phone_number) > 0 and not re.match(phone_number_format, phone_number, re.IGNORECASE):
            raise GatorConnectionError("Phone Number Format is incorrect, must be ###-###-####")

        try:
            housing_listing = HousingListingPost.objects.get(housing_id=housing_id)
        except HousingListingPost.DoesNotExist:
            raise GatorConnectionError("Something went wrong when sending the Housing Request, please try again later.")

        try:
            reg_user_id = request.session['reg_user_id']
            registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)
        except (KeyError, RegisteredUser.DoesNotExist) as e:
            raise ValidationError("You must be logged in to send a housing request.")


        # Create Housing request object and save it in database
        housing_request = HousingListingRequest()
        housing_request.housing_listing = housing_listing
        housing_request.registered_user = registered_user

        try:
            housing_request.save()
        except Exception as e:
            raise GatorConnectionError("Something went wrong when sending the Housing Request, please try again later.")

        # Create Housing List Form and save it in database
        housing_form = HousingListingForm()
        housing_form.about_me = about_me
        housing_form.move_in = move_in_date
        housing_form.registered_user = registered_user
        housing_form.housing_listing_request = housing_request
        housing_form.phone_number = phone_number

        housing_form.save()

        post_owner = housing_listing.post.registered_user

        

        try:
            post_owner_account = Account.objects.get(user=post_owner.user)
            reg_user_email = Account.objects.get(user=registered_user.user)
        except Account.DoesNotExist:
            raise GatorConnectionError('Post Owner account does not exist')
        
        move_date = str(move_in_date)

        email_content = f"""Dear {post_owner.first_name},\n\n
{registered_user.first_name} {registered_user.last_name} is interested in your housing listing. Here is his/her information:\n\n
His/Her Email: {reg_user_email.email}

His/Her Phone Number: {"Not Given" if len(phone_number) <= 0 else phone_number}

Preferred Move In Date: {move_date[0:10]}

About Him/Her:
{about_me}
        
If you feel that he/she is a good match, please get in contact with him/her.

Best,

Gator Connection
"""



        email_content_interested = 'You have made a request for ' + post_owner.first_name + "'s housing listing.  If the post owner feels that you are a good match, he/she will email you." + '\n\nBest,\n\nGator-Connection'

        notification = Notification()

        notification.registered_user = housing_listing.post.registered_user
        notification.message = f"{registered_user.first_name} {registered_user.last_name} is interested in your housing listing post."

        notification.save()

        housing_notification = HousingListingRequestNotification()
        housing_notification.notification = notification
        housing_notification.housing_listing_request = housing_request

        housing_notification.save()

        # Sends email to the user who posted the housing listing after filling out the form
        send_mail(
            'Housing Listing Interest!',
            email_content,
            'Do Not Reply | Gator-connection',
            [post_owner_account.email],
            fail_silently=False
        )

        # Sends email to the user who interested the item listing after filling out the form
        send_mail(
            'Housing Listing Interest!',
            email_content_interested,
            'Do Not Reply | Gator-connection',
            [reg_user_email.email],
            fail_silently=False
        )

    @staticmethod
    def deleteHousingRequest(request, housing_id):
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

        # Get Housing Listing Post object
        try:
            housing_listing = HousingListingPost.objects.get(housing_id=housing_id)
        except HousingListingPost.DoesNotExist:
            raise GatorConnectionError("This housing listing post no longer exists.")

        # Get requests of housing listing object that is a registered user
        try:
            housing_request = HousingListingRequest.objects.get(registered_user=registered_user,
                                                                housing_listing=housing_listing)
        except HousingListingRequest.DoesNotExist:
            raise GatorConnectionError("Error, your request already does not exist")

        housing_request.delete()

    @staticmethod
    def checkIfRequested(request, housing_post):
        try:
            reg_user_id = request.session['reg_user_id']
        except KeyError:
            return False

        # Check if registered user is not the one who posted
        if reg_user_id != housing_post.post.registered_user.reg_user_id:
            # Check if registered user already sent a request
            try:
                registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)
            except (RegisteredUser.DoesNotExist):
                return False

            try:
                housing_listing_request = HousingListingRequest.objects.get(registered_user=registered_user,
                                                                        housing_listing=housing_post)
            except HousingListingRequest.DoesNotExist:
                # Could not find a housing listing request, therefore, has not requested
                print("Could not find a housing request associated with the user, can make request")
                return False

            # Housing Listing Request exists, therefore, user has requested already
            print("Already made a housing request")
            return True

        # Else, registered user is the one who posted, so user can't request his/her own post
        else:
            return False

    @staticmethod
    def housingFormNotification(request, housing_post):
        # Will send email when a form for interest in housing is submitted
        pass

    @staticmethod
    def getHousingRequests(request):
        """

        :type request: HttpRequest
        :param request: The HttpRequest GET object that should contain the user identification data
        :return: An array of dictionarys with keys {"housing_request", "housing_form"}
        :rtype: list[dict]
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

        # Get housing listing requests for the housing listing posts that the registered user has posted
        housing_requests = HousingListingRequest.objects.filter(housing_listing__post__registered_user=registered_user)

        # For each housing listing request, get the corresponding housing request form
        for housing_request in housing_requests:
            try:
                housing_form = HousingListingForm.objects.get(housing_listing_request=housing_request)
            except HousingListingForm.DoesNotExist:
                # This should never happen
                print("Housing Request does not have a housing form")
                housing_form = None

            # Get the email of the user that requested as well
            try:
                account = Account.objects.get(user=housing_request.registered_user.user)
                email = account.email
            except Account.DoesNotExist:
                print("The registered user that requested does not have an account")
                email = None

            template_data.append({
                "housing_request": housing_request,
                "housing_form": housing_form,
                "email": email,
            })

        return template_data



