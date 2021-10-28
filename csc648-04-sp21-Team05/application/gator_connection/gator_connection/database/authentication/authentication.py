from gator_connection.models import *

from gator_connection.database.gator_connection_exceptions import *

from gator_connection.database.email_helper import EmailHelper
from gator_connection.database.make_confirm_string import MakeConfirmString

import re
#import bcrypt


class Authentication:

    # Separate Authentication into StudentAuthentication, AdminAuthentication, SuperUserAuthentication files

    @staticmethod
    def createAnonymousUser():
        user = User()
        user.save()
        return user

    @staticmethod
    def logout(request):
        # Delete all relevant identifying information in request.session
        if 'isSuperUser' in request.session:
            del request.session['super_user_id']
            del request.session['isSuperUser']
        elif 'isAdmin' in request.session:
            del request.session['admin_id']
            del request.session['isAdmin']
            del request.session['admin_position']
            del request.session['admin_type']
        elif 'isStudent' in request.session:
            del request.session['student_id']
            del request.session['isStudent']

        del request.session['reg_user_id']
        del request.session['is_loggedin']
        del request.session['first_name']
        del request.session['last_name']
        del request.session['email']
        del request.session['email_verified']
        # Return stripped down request with no privileges

        return request

    @staticmethod
    def getSession(request):

        if 'is_loggedin' in request.session:
            # User is a registered user and logged in
            pass
        elif 'user_id' in request.session:
            # User is unauthenticated/not registered, but has visited site recently
            print(request.session['user_id'])
            pass
        else:
            # Brand new user, create new anonymous user id
            print("create new anonymous user")
            user = Authentication.createAnonymousUser()
            # Add user_id to request.session
            request.session['user_id'] = user.user_id
        return request

    @staticmethod
    def checkEmailFormat(email):
        regex = r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"

        if re.search(regex, email, re.IGNORECASE):
            return True
        return False

    @staticmethod
    def checkUniqueEmail(email):
        # Check if email is unique
        try:
            emailCheck = Account.objects.get(email=email)

            if emailCheck:
                # Email already exists, throw unique email error
                raise UniqueEmailError(email)
        except Account.DoesNotExist:
            pass

    @staticmethod
    def checkGeneralAccountRegisterFormValidation(first_name, last_name):
        # Check if first name and last name fit in the database
        first_name_length = len(first_name)
        last_name_length = len(last_name)

        if first_name_length > 45:
            raise InvalidFormError(first_name,
                                   f"should be less than 45 characters. Current Length: {first_name_length}")

        if last_name_length > 45:
            raise InvalidFormError(last_name, f"should be less than 45 characters. Current Length: {last_name_length}")

    @staticmethod
    def checkGeneralLoginFormValidation(email, password):
        email_length = len(email)
        password_length = len(password)

        if email_length > 45:
            raise InvalidFormError(email,
                                   f"should be less than 45 characters. Current Length: {email_length}")
        if password_length > 45:
            raise InvalidFormError(password,
                                   f"should be less than 45 characters. Current Length: {password_length}")

        if not (Authentication.checkEmailFormat(email)):
            raise InvalidFormError(email, "is not an email.")

    @staticmethod
    def encryptPassword(password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(12))

    @staticmethod
    def checkPassword(password, stored):
        """
        Compares an unhashed/unencrypted password against the hashed/encrypted stored password. Returns true if passwords
        match. Only Authentication and its subclasses shall call this method.
        """
        # encrypted = Authentication.__encryptPassword(password)
        if bcrypt.checkpw(password.encode(), stored):
            return True
        else:
            return False

    @staticmethod
    def createAccountAndRegisteredUser(request, user_id, first_name, last_name, email, password):
        """Creates an Account and Registered User object and saves it in the database. Returns a tuple (
        registeredUser, account). Only Authentication and subclasses of Authentication should call this function.
        """
        # Get User object from database
        try:
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            user = Authentication.createAnonymousUser()

        try:
            registeredUserCheck = RegisteredUser.objects.get(user=user)

            if registeredUserCheck:
                # Registered User already exists for current user_id, need to generate a new user
                user = Authentication.createAnonymousUser()
                request.session['user_id'] = user.user_id
        except RegisteredUser.DoesNotExist:
            pass

        registeredUser = Authentication.__createRegisteredUser(user, first_name, last_name)

        account = Account()
        account.email = email
        account.password = password
        account.user = user

        account.save()

        code = MakeConfirmString.make_confirm_string(account)
        EmailHelper.send_email(email, first_name, code, 1)

        notification = Notification()
        notification.registered_user = registeredUser
        notification.message = "You must verify your email in order to use Gator Connection's Features."

        return (registeredUser, account)

    @staticmethod
    def __createRegisteredUser(user, first_name, last_name):
        """
        Creates a registered user object and saves it in the database. Returns the saved registered user object. Only
        the Authentication class shall call this method. This method is private.
        """
        registeredUser = RegisteredUser()
        registeredUser.user = user
        registeredUser.first_name = first_name
        registeredUser.last_name = last_name

        registeredUser.save()

        return registeredUser
