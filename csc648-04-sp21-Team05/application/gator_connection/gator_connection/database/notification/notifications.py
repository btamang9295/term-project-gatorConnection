from gator_connection.models import *

from gator_connection.database.gator_connection_exceptions import *


class Notifications:
    """
    A class that abstracts database interactions for Notification such as retrieving Notification
    and checking Notification.

    **Methods:**
    - getNotifications(request)
    - checkNotifications(request)

    """

    @staticmethod
    def getNotifications(request):
        """
        This function takes in a HttpRequest GET object. Retrieves all notification of log_in registered user
        from our Gator Connection database, and update those notification's attributes of "Read" 
        be True into the database.

        :type request: HttpRequest
        :param request: The HttpRequest GET object that should contain the user identification data
        :return: An array of Notification objects
        :rtype: list[Notification]
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

        # Get item listing requests for the item listing posts that the registered user has posted
        notifications = Notification.objects.filter(registered_user=registered_user)
        notifications.update(read=True)

        return notifications

    @staticmethod
    def checkNotifications(request):
        """
        This function takes in a HttpRequest GET object. Get 'unread' notification of log_in registered user.
        If 'unread' notification existed, return Ture. 

        :type request: HttpRequest
        :param request: The HttpRequest GET object that should contain the user identification data
        :return: Boolean value indicating whether user has unread notifications
        :rtype: bool
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

        unreadNotifications = Notification.objects.filter(registered_user=registered_user, read=False).count()

        return unreadNotifications > 0




    # @staticmethod
    # def get_queryset(request):
    #     try:
    #         reg_user_id = request.session['reg_user_id']
    #     except KeyError:
    #         raise GatorConnectionError(
    #             "There is an error, you are not authenticated. Please log out and log back in and retry.")
    #
    #     # Get registered user object
    #     try:
    #         registered_user = RegisteredUser.objects.get(reg_user_id=reg_user_id)
    #     except RegisteredUser.DoesNotExist:
    #         raise GatorConnectionError("There is an error, you are not authenticated.")
    #
    #     notifications = Notification.objects.filter(registered_user=registered_user)
    #     notifications.update(read=True)
    #     return notifications