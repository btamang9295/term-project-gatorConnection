"""
This class is for inserting new devices into the database and checking that a device that a user logged in with is new or not
"""
from uuid import UUID, uuid4


from gator_connection.models import *
from gator_connection.database.gator_connection_exceptions import *
from gator_connection.database.email_helper import EmailHelper

from django.db.models.functions import Now


class DeviceAuth:

    @staticmethod
    def checkDevice(request, registered_user):
        # Get the device's identification number that Gator Connection provided on login
        device_uuid = request.session.get('device')


        if not device_uuid:
            # Assume that user is logging into a new device
            # This also could be caused by a user's browser clearing cookies
            return DeviceAuth.createDevice(request, registered_user)

        # This device has a UUID given by Gator Connection

        # Need to check if this device belongs to the registered_user
        # Get device from database
        try:
            device = Device.objects.get(uuid=device_uuid)
        except Device.DoesNotExist:
            # Device doesn't exist
            return DeviceAuth.createDevice(request, registered_user)

        try:
            user_device = UserDevice.objects.get(device=device, registered_user=registered_user)
        except UserDevice.DoesNotExist:
            # This device does not belong to this user

            user_device = UserDevice()

            user_device.device = device
            user_device.registered_user = registered_user

            user_device.save()

            return DeviceAuth.sendDeviceAuthEmail(request, registered_user)

        # This is a device that belongs to this user, update used_at field
        return request



    @staticmethod
    def createDevice(request, registered_user, register=False):
        """This function will create a new device in the database, add it to one of the registered user's devices"""
        # Create new device object in database


        uuid = uuid4()

        # Make sure the uuid does not exist in the database
        while True:
            try:
                check_unique = Device.objects.get(uuid=str(uuid))
                uuid = uuid4()
            except Device.DoesNotExist:
                break



        device = Device()
        device.uuid = str(uuid)
        device.save()

        request.session['device'] = device.uuid


        # Set User and Device relation
        user_device = UserDevice()
        user_device.registered_user = registered_user
        user_device.device = device

        user_device.save()

        if not register:
            DeviceAuth.sendDeviceAuthEmail(request, registered_user)

        return request

    @staticmethod
    def sendDeviceAuthEmail(request, registered_user):
        # Get the email of the registered_user, need to get account first
        try:
            account = Account.objects.get(user=registered_user.user)
        except Account.DoesNotExist:
            raise GatorConnectionError("You do not have an account.")

        EmailHelper.send_email(account.email, registered_user.first_name, None, 5)

        return request






