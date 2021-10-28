from gator_connection.models import *

from gator_connection.database.gator_connection_exceptions import *

from gator_connection.database.search import Search


class Announcements:

    """
    A class that abstracts database interactions for Announcements such as retrieving Announcements,
    saving Announcements, editing Announcements, and searching Announcements.

    **Methods:**
    - postAnnouncement(request, category)
    - editAnnouncement(request, announcement_id)
    - deleteAnnouncement(request, announcement_id)
    - getAllAnnouncements()
    - getAnnouncementsFromCategory(category)
    - getAnnouncement(announcement_id)
    - __extractAnnouncementPostRequestData(request)
    - __saveImage(post, image_path)

    """

    @staticmethod
    def postAnnouncement(request, category):
        """
        This function takes in a HttpRequest POST object. Extracts all of the necessary data to fill the fields in
        our Gator Connection database. Creates a Announcement Post Django ORM object and uses Django's built-in
        ORM features to save the object created from the information in the HttpRequest POST object into the database.

        :type request: HttpRequest
        :param request: Should be a POST HttpRequest object that contains values from the Announcement Form
        :return: None
        :raises GatorConnectionError: If data from Announement is invalid or missing
        """
        try:
            requestData = Announcements.__extractAnnouncementPostRequestData(request)
        except GatorConnectionError as e:
            raise e

        try:
            image_path = request.FILES.get('image_path')
        except AttributeError:
            image_path = None

        # Create Post Object and store it in database
        post = Post()

        post.title = requestData.get('title')
        post.description = requestData.get('description')
        post.registered_user = requestData.get('registered_user')

        post.save()

        # Create Announcement Object and store it in database
        announcement = Announcement()
        announcement.admin = requestData.get('admin_account')
        announcement.post = post
        announcement.category = category

        announcement.save()

        # Create image if user uploaded one
        Announcements.__saveImage(post, image_path)

    @staticmethod
    def editAnnouncement(request, announcement_id):
        """
        This function takes in a HttpRequest POST object and the id of an announcement. Extracts all of the necessary
        data in the request object to fill the fileds in our Gator Connection database. Queries the database for an
        existing Announcement Post using the *announcement_id* using Django's built-in ORM. Then it uses the extracted
        data from the HttpRequest POST object and updates the values of the Announcement Post object. Then it
        saves the newly updated Housing Listing Post object into the database.

        :type request: HttpRequest
        :param request: Should be a POST HttpRequest object that contains values from the Edit Housing Listing Form
        :type announcement_id: int
        :param announcement_id: The ID of the Housing Listing in the database that you would like to edit.
        :return: None
        :raises GatorConnectionError: If data from Request Announcment Form is invalid or missing
        """
        try:
            requestData = Announcements.__extractAnnouncementPostRequestData(request)
        except GatorConnectionError as e:
            raise e

        try:
            image_path = request.FILES.get('image_path')
        except AttributeError:
            image_path = None

        # Get the corresponding announcement
        try:
            announcement = Announcement.objects.get(announcement_id=announcement_id)
        except Announcement.DoesNotExist:
            raise GatorConnectionError("Something went wrong, this announcement no longer exists.")

        announcement.post.title = requestData.get('title')
        announcement.post.description = requestData.get('description')
        announcement.post.save()

        announcement.save()

        Announcements.__saveImage(announcement.post, image_path)

    @staticmethod
    def deleteAnnouncement(request, announcement_id):
        """
        This function takes in a HttpRequest POST object and the id of a announcement. This function validates
        the user that requested to delete the housing listing post corresponding to *announcement_id* using Django's
        Sessions middleware. If the user is authenticated and the one that posted the announcement, this function
        queries the database for the announcement post using the *announcement_id*. Then it uses Django's ORM
        delete() function to delete the announcement Post from the database.

        :type request: HttpRequest
        :param request: Should be a POST HttpRequest object
        :type announcement_id: int
        :param announcement_id: The ID of the announcement in the database that has been requested to be deleted
        :return: None
        :raises GatorConnectionError: If user that made request is
        not authenticated, not the user that posted the announcement or the announcement post that was
        requested to be deleted doesn't exist
        """
        try:
            reg_user_id = request.session['reg_user_id']
            registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)
        except (KeyError, RegisteredUser.DoesNotExist):
            raise GatorConnectionError("You are not validated. Please log out and log back in again and retry.")

        try:
            announcement = Announcement.objects.get(announcement_id=announcement_id)
        except Announcement.DoesNotExist:
            raise GatorConnectionError(
                "Something went wrong, this announcement no longer exists. Failed successfully :D")

        if announcement.post.registered_user != registered_user:
            raise GatorConnectionError(
                "You are not the owner of this announcement. You are forbidden from deleting this post.")

        announcement.delete()

    @staticmethod
    def getAllAnnouncements():
        """
        This function is a helper function for *getAnnouncementsFromCategory()*. This function uses Django's ORM to get all rows in
        the Announcement table in our database. Because this table does not have all of the data needed for
        rendering on the frontend, for each row returned from the database, this function queries for the corresponding
        post and images. Then this function builds a dictionary to return to the frontend for easy access.

        :return: An array of dictionaries with keys {"athletics", "department", "organization"}
        :rtype: list[dict]
        """
        template_data = {
            "athletics": Announcements.getAnnouncementsFromCategory("Athletics"),
            "department": Announcements.getAnnouncementsFromCategory("Department"),
            "organization": Announcements.getAnnouncementsFromCategory("Organization")
        }

        return template_data

    @staticmethod
    def getAnnouncementsFromCategory(category):
        announcements = Announcement.objects.filter(category=category)

        template_data = []

        for announcement in announcements:

            # Get the specific admin account type associated with the announcement
            admin_type_account = None

            if category == "Athletics":
                admin_type_account = AthleticsAccount.objects.get(admin_account=announcement.admin)
            elif category == "Department":
                admin_type_account = DepartmentAccount.objects.get(admin_account=announcement.admin)
            elif category == "Organization":
                admin_type_account = OrganizationAccount.objects.get(admin_account=announcement.admin)

            # Get any images associated with the announcement
            try:
                images = Image.objects.filter(post=announcement.post)
            except Image.DoesNotExist:
                images = None

            template_data.append(
                {
                    "announcement": announcement,
                    "images": images,
                    "registered_user": announcement.post.registered_user,
                }
            )

        return template_data

    @staticmethod
    def getAnnouncement(announcement_id):
        # Get specific announcement
        try:
            announcement = Announcement.objects.get(announcement_id=announcement_id)
        except Announcement.DoesNotExist:
            raise GatorConnectionError("Something went wrong, announcement does not exist.")

        # Get any images associated with the announcement
        try:
            images = Image.objects.filter(post=announcement.post)
        except Image.DoesNotExist:
            images = None

        # Get the admin type account associated with the announcement
        admin_type_account = None
        try:
            admin_type_account = AthleticsAccount.objects.get(admin_account=announcement.admin)
        except AthleticsAccount.DoesNotExist:
            pass

        try:
            admin_type_account = DepartmentAccount.objects.get(admin_account=announcement.admin)
        except DepartmentAccount.DoesNotExist:
            pass

        try:
            admin_type_account = OrganizationAccount.objects.get(admin_account=announcement.admin)
        except OrganizationAccount.DoesNotExist:
            pass

        return {
            "announcement": announcement,
            "images": images,
            "registered_user": announcement.post.registered_user,
        }

    @staticmethod
    def __extractAnnouncementPostRequestData(request):
        # Get all announcement information from request
        title = request.POST.get('title')
        description = request.POST.get('description')

        try:
            registered_user = request.session['reg_user_id']
        except KeyError:
            raise ValidationError("You must be logged in to an admin account to post announcements.")

        # Check if user is logged in
        try:
            registered_user = RegisteredUser.objects.get(reg_user_id=registered_user)
        except RegisteredUser.DoesNotExist:
            raise ValidationError("You must be logged in to an admin account to post announcements.")

        # Check if user is an admin
        try:
            print(request.session['isAdmin'])
            if request.session['isAdmin'] == True:
                pass

            admin_account = AdminAccount.objects.get(admin_account_id=request.session['admin_id'])

        except (KeyError, AdminAccount.DoesNotExist) as e:
            # Could not find property isAdmin, therefore, not an admin
            raise ValidationError("You must be an admin to post announcements.")

        # Check if title will fit in database
        title_length = len(title)

        if title_length > 45:
            raise InvalidFormError(title, f"should be less than 45 characters long. Current Length: {title_length}")

        requestData = {
            "title": title,
            "description": description,
            "registered_user": registered_user,
            "admin_account": admin_account,
        }

        return requestData

    @staticmethod
    def __saveImage(post, image_path):
        if image_path is None:
            return
        # Create Image Object and store it in database
        image = Image()

        image.image_path = image_path
        image.post = post
        image.save()
