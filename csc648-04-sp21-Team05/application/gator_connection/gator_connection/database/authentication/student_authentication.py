from gator_connection.database.authentication.authentication import Authentication
from gator_connection.database.gator_connection_exceptions import *
from gator_connection.database.authentication.device import DeviceAuth

from gator_connection.models import *

from datetime import datetime

from django.utils.timezone import make_aware


class StudentAuthentication(Authentication):

    @staticmethod
    def registerStudent(request):
        # FINISHED:
        # - Add check for unique email
        # - Add check if user_id already has an account, then need to generate a new user id
        # - Validated email, first_name, last_name fields

        # FIXME: validate all form fields, add to device session tables, add error handling for failed database insert

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = Authentication.encryptPassword(request.POST.get('password'))
        email = request.POST.get('email')

        try:
            graduation_month = datetime.strptime(request.POST.get('graduation_date'), "%Y-%m-%d")

            if graduation_month.date() < datetime.now().date():
                raise GatorConnectionError("Cannot go back in time. Please enter a valid future date.")
            graduation_month = make_aware(graduation_month)
        except ValueError:
            raise GatorConnectionError("Date Format is incorrect, must be YYYY-MM-DD.")

        # Backend Student Account Form Validation
        try:
            Authentication.checkGeneralAccountRegisterFormValidation(first_name, last_name)
            StudentAuthentication.checkStudentEmail(email)

        except GatorConnectionError as e:
            raise e

        # Get user_id from request.session
        user_id = request.session['user_id']

        # Create new Account and Registered User object with user as foreign key
        (registered_user, account) = Authentication.createAccountAndRegisteredUser(request, user_id, first_name,
                                                                                  last_name, email, password)

        # Create new StudentAccount object with account as foreign key
        studentAccount = StudentAuthentication.__createStudentAccount(account, graduation_month)

        # If all inserts succeed, then add identification to request.session
        request.session['isStudent'] = True
        request.session['student_id'] = studentAccount.student_id
        request.session['first_name'] = registered_user.first_name
        request.session['last_name'] = registered_user.last_name
        request.session['reg_user_id'] = registered_user.reg_user_id
        request.session['is_loggedin'] = True
        request.session['is_verified'] = False
        request.session['email'] = account.email
        request.session['email_verified'] = account.email_verified

        request = DeviceAuth.createDevice(request, registered_user, True)

        return request

    @staticmethod
    def authenticateStudent(request):
        # Extract login information from request
        email = request.POST.get('sfsu_email')
        password = request.POST.get('password')

        try:
            Authentication.checkGeneralLoginFormValidation(email, password)
            StudentAuthentication.checkStudentEmailFormat(email)
        except GatorConnectionError as e:
            raise e

        # Get Student Account from database
        try:
            account = Account.objects.get(email=email)
            studentAccount = StudentAccount.objects.get(account=account)
        except Account.DoesNotExist:
            raise InvalidFormError(email, "does not exist. Please register or try a different email.")
        except StudentAccount.DoesNotExist:
            raise InvalidFormError(email,
                                   "is not a Student Account. Please choose the correct account type that the "
                                   "email was registered under.")

        # Get Registered User from database
        registered_user = RegisteredUser.objects.select_related().get(user_id=studentAccount.account.user.user_id)

        # Now that we have Registered User and Student Account, check password with Student Account

        # if we want to ban user log in before they finish email_verification
        # if not account.email_verified:
        #     raise NotVerified()
        #     return render(request, '/home')

        if Authentication.checkPassword(password, account.password):
            # Add identification data to request.session
            request.session['user_id'] = account.user.user_id
            request.session['reg_user_id'] = registered_user.reg_user_id
            request.session['student_id'] = studentAccount.student_id
            request.session['is_loggedin'] = True
            request.session['first_name'] = registered_user.first_name
            request.session['last_name'] = registered_user.last_name
            request.session['email'] = account.email
            request.session['email_verified'] = account.email_verified

            request = DeviceAuth.checkDevice(request, registered_user)
        else:
            raise ValidationError()

        return request

    @staticmethod
    def checkStudentEmailFormat(email):
        # Check if email length will fit in database
        email_length = len(email)
        if email_length > 45:
            raise InvalidFormError(email, f"should be less than 45 characters. Current Length: {email_length}")

        # Check if email is an sfsu email
        if not ("@mail.sfsu.edu" in email) and not ("@sfsu.edu" in email):
            if (Authentication.checkEmailFormat(email)):
                # Not a correctly formatted email
                raise InvalidFormError(email, "is not an SFSU email.")

            raise InvalidFormError(email, "is not an email.")

    @staticmethod
    def checkStudentEmail(email):
        try:
            StudentAuthentication.checkStudentEmailFormat(email)
        except GatorConnectionError as e:
            raise e

        Authentication.checkUniqueEmail(email)

    @staticmethod
    def __createStudentAccount(account, graduation_date):
        studentAccount = StudentAccount()
        studentAccount.graduation_month = graduation_date
        studentAccount.account = account
        studentAccount.save()

        return studentAccount
