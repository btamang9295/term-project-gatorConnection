from gator_connection.database.gator_connection_exceptions import *
from gator_connection.models import *

from gator_connection.database.restaurants.restaurant import Restaurants


class SuperUserTools:
    """
    A class that abstracts database interactions for Super User such as 
    Approve or Reject the Super user request and the RestaurantRequest.

    **Methods:**
    - approveSuperUser(superuser_id)
    - approveAdmin(admin_id)
    - approveRestaurantRequest(restaurant_request_id)
    - rejectSuperUser(superuser_id)
    - rejectAdmin(admin_id)
    - rejectRestaurantRequest(restaurant_request_id)

    """
    @staticmethod
    def approveSuperUser(superuser_id):
        """
        This function are managing the Super User approed.

        :type superuser_id: int
        :param superuser_id: The requested SuperUserAccount to retrieve from the database
        :raises:GatorConnectionError : If data from SuperUserAccount is invalid or missing
        """
        try:
            super_user = SuperUserAccount.objects.get(super_user_id=superuser_id)

            # Approve Super User
            super_user.is_approved = True

            super_user.save()

        except SuperUserAccount.DoesNotExist:
            raise GatorConnectionError("Super User Account Request Does Not Exist")

    @staticmethod
    def approveAdmin(admin_id):
        """
        This function are managing the Admin approed.

        :type admin_id: int
        :param admin_id: The requested AdminAccount to retrieve from the database
        :raises:GatorConnectionError : If data from AdminAccount is invalid or missing
        """
        try:
            admin = AdminAccount.objects.get(admin_account_id=admin_id)

            # Approve Admin
            admin.is_approved = True

            admin.save()

        except AdminAccount.DoesNotExist:
            raise GatorConnectionError("Admin Account Request Does Not Exist")

    @staticmethod
    def approveRestaurantRequest(restaurant_request_id):
        """
        This function are managing the RestaurantRequest approed.

        :type restaurant_request_id: int
        :param restaurant_request_id: The requested RestaurantRequest to retrieve from the database
        :raises:GatorConnectionError : If data from RestaurantRequest is invalid or missing
        """
        try:
            restaurant_request = RestaurantRequest.objects.get(restaurant_request_id=restaurant_request_id)

            Restaurants.postRestaurant(restaurant_request)
        except RestaurantRequest.DoesNotExist:
            raise GatorConnectionError("Restaurant Request Does Not Exist")

    @staticmethod
    def rejectSuperUser(superuser_id):
        """
        This function are managing the Super User approed.

        :type superuser_id: int
        :param superuser_id: The requested SuperUserAccount to retrieve from the database
        :raises:GatorConnectionError : If data from SuperUserAccount is invalid or missing
        """
        try:
            # Delete User associated with Super User account so database will cascade delete everything associated with
            # the account
            super_user = SuperUserAccount.objects.get(super_user_id=superuser_id)

            # Get User associated with Super User account
            user = super_user.account.user

            user.delete()

        except SuperUserAccount.DoesNotExist:
            raise GatorConnectionError("Super User Account Request Does Not Exist")

    @staticmethod
    def rejectAdmin(admin_id):
        """
        This function are managing the Admin approed.

        :type admin_id: int
        :param admin_id: The requested AdminAccount to retrieve from the database
        :raises:GatorConnectionError : If data from AdminAccount is invalid or missing
        """
        try:
            # Delete User associated with Admin account so database will cascade delete everything
            admin = AdminAccount.objects.get(admin_account_id=admin_id)

            # Get User associated with Admin account
            user = admin.account.user

            user.delete()

        except AdminAccount.DoesNotExist:
            raise GatorConnectionError("Admin Account Request Does Not Exist")

    @staticmethod
    def rejectRestaurantRequest(restaurant_request_id):
        """
        This function are managing the RestaurantRequest approed.

        :type restaurant_request_id: int
        :param restaurant_request_id: The requested RestaurantRequest to retrieve from the database
        :raises:GatorConnectionError : If data from RestaurantRequest is invalid or missing
        """
        try:
            # Delete the Post associated with restaurant_request_id so database will delete notifications as well
            restaurant_request = RestaurantRequest.objects.get(restaurant_request_id=restaurant_request_id)

            # Get the post associated with restaurant_request
            post = restaurant_request.post

            post.delete()

        except RestaurantRequest.DoesNotExist:
            raise GatorConnectionError("Restaurant Request Does Not Exist")
