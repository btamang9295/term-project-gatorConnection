from gator_connection.database.authentication.authentication import Authentication
from gator_connection.database.gator_connection_exceptions import *
from gator_connection.database.authentication.device import DeviceAuth


from gator_connection.models import *


class SuperUserAuthentication(Authentication):

    @staticmethod
    def registerSuperUser(request):
        # Get registration info from request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = Authentication.encryptPassword(request.POST.get('password'))
        email = request.POST.get('email')

        # Backend Super User Account form validation
        try:
            Authentication.checkGeneralAccountRegisterFormValidation(first_name, last_name)

            # Check length of email to make sure it will fit in database
            email_length = len(email)

            if email_length > 45:
                raise InvalidFormError(email, f"should be less than 45 characters long. Current Length: {email_length}")

            if not (Authentication.checkEmailFormat(email)):
                raise InvalidFormError(email, "is not an email.")

            Authentication.checkUniqueEmail(email)


        except GatorConnectionError as e:
            raise e

        # Get user_id from request.session
        user_id = request.session['user_id']

        # Create new Account and Registered User object with user as a foreign key
        (registered_user, account) = Authentication.createAccountAndRegisteredUser(request, user_id, first_name,
                                                                                  last_name, email, password)

        superUserAccount = SuperUserAuthentication.__createSuperUserAccount(account)

        # If all inserts succeed, then add identification to request.session
        request.session['isSuperUser'] = True
        request.session['super_user_id'] = superUserAccount.super_user_id
        request.session['first_name'] = registered_user.first_name
        request.session['last_name'] = registered_user.last_name
        request.session['reg_user_id'] = registered_user.reg_user_id
        request.session['is_loggedin'] = True
        request.session['is_verified'] = False
        request.session['email'] = account.email
        request.session['email_verified'] = account.email_verified
        request.session['is_approved'] = superUserAccount.is_approved

        request = DeviceAuth.createDevice(request, registered_user, True)

        return request

    @staticmethod
    def authenticateSuperUser(request):
        # Extract login information from request
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            Authentication.checkGeneralLoginFormValidation(email, password)
        except GatorConnectionError as e:
            raise e

        # Get Super User Account from database
        try:
            account = Account.objects.get(email=email)
            superUserAccount = SuperUserAccount.objects.get(account=account)
        except Account.DoesNotExist:
            raise InvalidFormError(email, "does not exist. Please register or try a different email.")
        except SuperUserAccount.DoesNotExist:
            raise InvalidFormError(email,
                                   "is not a Super User Account. Please choose the correct account type that the email was registered under.")

        # Get Registered User from database
        registered_user = RegisteredUser.objects.select_related().get(user_id=account.user.user_id)

        # Now that we have Registered User and Super User Account, check password with Super User Account

        if Authentication.checkPassword(password, account.password):
            # Add identification data to request.session
            request.session['isSuperUser'] = True
            request.session['user_id'] = account.user.user_id
            request.session['reg_user_id'] = registered_user.reg_user_id
            request.session['super_user_id'] = superUserAccount.super_user_id
            request.session['is_loggedin'] = True
            request.session['first_name'] = registered_user.first_name
            request.session['last_name'] = registered_user.last_name
            request.session['email'] = account.email
            request.session['email_verified'] = account.email_verified
            request.session['is_approved'] = superUserAccount.is_approved

            request = DeviceAuth.checkDevice(request, registered_user)
        else:
            raise ValidationError()

        return request

    @staticmethod
    def __createSuperUserAccount(account):
        superUserAccount = SuperUserAccount()
        superUserAccount.account = account

        superUserAccount.save()

        return superUserAccount

    @staticmethod
    def getAllSuperUserAccountRequests(request):

        # Make sure the user requesting this is logged in, is approved by a super user, and is email verified
        sessionAttributes = request.session.keys()
        if ('is_loggedin' in sessionAttributes) and ('is_approved' in sessionAttributes) and (
                'email_verified' in sessionAttributes):
            # Make sure all of these identification attributes are true
            if (request.session['is_loggedin']) and (request.session['is_approved']) and (
            request.session['email_verified']):

                template_data = []

                # Have identified user as trustworthy Super User, can get Super User Account requests
                superUserAccounts = SuperUserAccount.objects.filter(is_approved=False)

                for superUserAccount in superUserAccounts:
                    # Get the user associated with each super user account
                    user = superUserAccount.account.user

                    # Get the registered user associated with the user so that we have access to the name
                    try:
                        registered_user = RegisteredUser.objects.get(user=user)
                    except RegisteredUser.DoesNotExist:
                        # This should never occur, but can't let this crash system
                        registered_user = None

                    template_data.append({
                        "superuser_account": superUserAccount,
                        "registered_user": registered_user
                    })

                return template_data
            else:
                raise GatorConnectionError(
                    "Error: You must be a Super User who has verified his/her email and been approved by another Super User to use Super User Tools.")

        else:
            raise GatorConnectionError(
                "Error: You must be a Super User who has verified his/her email and been approved by another Super User to Use Super User Tools.")
