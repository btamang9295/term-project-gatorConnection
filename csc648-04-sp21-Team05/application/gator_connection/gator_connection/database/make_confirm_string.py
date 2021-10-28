from gator_connection.models import *
import uuid


class MakeConfirmString:
    """
    This is a class that help Email verification to create and save the random code.

    **Methods:**
    - make_confirm_string(account)
    """
    @staticmethod
    def make_confirm_string(account):
        """
        This helper function to create the random code for email verification.

        :type account: int
        :param account: the account id from database to request to post Email Verification.
        :return code: this is a random String
        :rtype:str
        """
        code = str(uuid.uuid4()).replace('-', '')
        print()
        EmailVerification.objects.create(code=code, account=account)
        return code
