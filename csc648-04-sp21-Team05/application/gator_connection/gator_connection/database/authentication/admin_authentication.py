from gator_connection.database.authentication.authentication import Authentication
from gator_connection.database.gator_connection_exceptions import *

from gator_connection.database.authentication.device import DeviceAuth

from gator_connection.models import *


class AdminAuthentication(Authentication):

    @staticmethod
    def registerAdmin(request):

        # Get registration info from request
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = Authentication.encryptPassword(request.POST.get('password'))
        email = request.POST.get('email')
        admin_type = request.POST.get('admin_type')
        organization = request.POST.get('organization')
        admin_position = request.POST.get('admin_position')

        # Backend Admin Account Form Validation
        try:
            Authentication.checkGeneralAccountRegisterFormValidation(first_name, last_name)
            Authentication.checkEmailFormat(email)

            # Check to make sure admin_position and organization field can fit in database
            admin_position_length = len(admin_position)
            organization_length = len(organization)

            if admin_position_length > 45:
                raise InvalidFormError(admin_position,
                                       f"should be less than 45 characters. Current Length: {admin_position_length}")
            if organization_length > 45:
                raise InvalidFormError(organization,
                                       f"should be less than 45 characters. Current Length: {organization_length}")

            Authentication.checkUniqueEmail(email)
        except GatorConnectionError as e:
            raise e

        # Get user_id from request.session
        user_id = request.session['user_id']

        # Create new Account and Registered User object with user as a foreign key
        (registered_user, account) = Authentication.createAccountAndRegisteredUser(request, user_id, first_name,
                                                                                  last_name, email, password)

        # Create new AdminAccount object with account as foreign key
        (adminAccount, adminTypeAccount) = AdminAuthentication.__createAdminAccount(account, admin_position, admin_type,
                                                                                    organization)

        # If all inserts succeed, then add identification to request.session
        request.session['isAdmin'] = True
        request.session['admin_type'] = admin_type
        request.session['organization'] = organization
        request.session['admin_position'] = admin_position
        request.session['admin_id'] = adminAccount.admin_account_id
        request.session['first_name'] = registered_user.first_name
        request.session['last_name'] = registered_user.last_name
        request.session['reg_user_id'] = registered_user.reg_user_id
        request.session['is_loggedin'] = True
        request.session['is_verified'] = False
        request.session['email'] = account.email
        request.session['email_verified'] = account.email_verified
        request.session['is_approved'] = adminAccount.is_approved

        request = DeviceAuth.createDevice(request, registered_user, True)

        return request

    @staticmethod
    def authenticateAdmin(request):
        # Extract login information from request
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin_type = request.POST.get('admin_type')

        try:
            Authentication.checkGeneralLoginFormValidation(email, password)
        except GatorConnectionError as e:
            raise e

        # Get Admin Account from database
        try:
            account = Account.objects.get(email=email)
            adminAccount = AdminAccount.objects.get(account=account)
        except Account.DoesNotExist:
            raise InvalidFormError(email, "does not exist. Please register or try a different email.")
        except AdminAccount.DoesNotExist:
            raise InvalidFormError(email,
                                   "is not a Admin Account. Please choose the correct account type that the email was registered under.")

        # Get the corresponding Department, Organization, or Athletics Account
        try:
            organization = None

            if admin_type == 'Athletics':
                athleticsAccount = AthleticsAccount.objects.get(admin_account=adminAccount)
                organization = athleticsAccount.sport
            elif admin_type == 'Department':
                departmentAccount = DepartmentAccount.objects.get(admin_account=adminAccount)
                organization = departmentAccount.name
            elif admin_type == 'Organization':
                organizationAccount = OrganizationAccount.objects.get(admin_account=adminAccount)
                organization = organizationAccount.name
        except (AthleticsAccount.DoesNotExist, DepartmentAccount.DoesNotExist, OrganizationAccount.DoesNotExist) as e:
            raise InvalidFormError(email,
                                   f"is not a(n) {admin_type} Account. Please choose the correct admin type that the email was registered under.")

        # Get Registered User from database
        registered_user = RegisteredUser.objects.select_related().get(user_id=adminAccount.account.user.user_id)

        # Now that we have Registered User and Admin Account, check password with Admin Account
        if Authentication.checkPassword(password, adminAccount.account.password):
            # Add identification data to request.session
            request.session['isAdmin'] = True
            request.session['user_id'] = adminAccount.account.user.user_id
            request.session['reg_user_id'] = registered_user.reg_user_id
            request.session['admin_id'] = adminAccount.admin_account_id
            request.session['organization'] = organization
            request.session['admin_type'] = admin_type
            request.session['admin_position'] = adminAccount.position
            request.session['is_loggedin'] = True
            request.session['first_name'] = registered_user.first_name
            request.session['last_name'] = registered_user.last_name
            request.session['email'] = account.email
            request.session['email_verified'] = account.email_verified
            request.session['is_approved'] = adminAccount.is_approved

            request = DeviceAuth.checkDevice(request, registered_user)
        else:
            raise ValidationError()

        return request

    @staticmethod
    def __createAdminAccount(account, position, admin_type, organization):

        # Create adminAccount object and save in database
        admin_account = AdminAccount()
        admin_account.position = position
        admin_account.account = account

        admin_account.save()

        admin_type_account = None
        if admin_type == "Organization":
            admin_type_account = AdminAuthentication.__createOrganizationAccount(organization, admin_account)
        elif admin_type == "Department":
            admin_type_account = AdminAuthentication.__createDepartmentAccount(organization, admin_account)
        elif admin_type == "Athletics":
            admin_type_account = AdminAuthentication.__createAthleticsAccount(organization, admin_account)

        return admin_account, admin_type_account

    @staticmethod
    def __createOrganizationAccount(organization, admin_account):
        organization_account = OrganizationAccount()
        organization_account.admin_account = admin_account
        organization_account.name = organization

        organization_account.save()
        return organization_account

    @staticmethod
    def __createDepartmentAccount(organization, admin_account):
        department_account = DepartmentAccount()
        department_account.admin_account = admin_account
        department_account.name = organization

        department_account.save()
        return department_account

    @staticmethod
    def __createAthleticsAccount(organization, admin_account):
        athletics_account = AthleticsAccount()
        athletics_account.admin_account = admin_account
        athletics_account.sport = organization

        athletics_account.save()
        return athletics_account

    @staticmethod
    def getAllAdminAccountRequests(request):

        # Make sure the user requesting this is logged in, is approved by a super user, and is email verified
        sessionAttributes = request.session.keys()
        if ('is_loggedin' in sessionAttributes) and ('is_approved' in sessionAttributes) and (
                'email_verified' in sessionAttributes):
            # Make sure all of these identification attributes are true
            if (request.session['is_loggedin']) and (request.session['is_approved']) and (
                    request.session['email_verified']):

                template_data = []

                # Have identified user as trustworthy Super User, can get Admin Account requests
                adminAccounts = AdminAccount.objects.filter(is_approved=False)

                for adminAccount in adminAccounts:
                    # Get the user associated with each Admin account
                    user = adminAccount.account.user

                    # Get the registered user associated with the user so that we have access to the name
                    try:
                        registered_user = RegisteredUser.objects.get(user=user)
                    except RegisteredUser.DoesNotExist:
                        # This should never occur, but can't let this crash system
                        registered_user = None

                    template_data.append({
                        "admin_account": adminAccount,
                        "registered_user": registered_user
                    })

                return template_data
            else:
                raise GatorConnectionError(
                    "Error: You must be a Super User who has verified his/her email and been approved by another Super User.")

        else:
            raise GatorConnectionError(
                "Error: You must be a Super User who has verified his/her email and been approved by another Super User.")
