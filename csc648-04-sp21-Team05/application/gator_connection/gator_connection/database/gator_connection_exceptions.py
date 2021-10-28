"""
Here classes that implement the Error notification in the page.

**Classes::**
- GatorConnectionError(Exception)
- ValidationError(GatorConnectionError)
- UniqueEmailError(GatorConnectionError):
"""

class GatorConnectionError(Exception):
    """
    This class are get the raise and notify user the error

    :type Exception: raises
    :param Exception; the error due to information missing are invalid
    :rtype:message
    """
    def __init__(self, message):
        self.__message = message
        super().__init__(message)

    def getMessage(self):
        return self.__message


class ValidationError(GatorConnectionError):
    """
    This class are get the raise and notify user the error

    :type GatorConnectionError: raises
    :param GatorConnectionError; the error due to information missing are invalid
    :rtype:message
    """
    def __init__(self, message="Email or password is incorrect"):
        super().__init__(message)


class UniqueEmailError(GatorConnectionError):
    """
    This class are get the raise and notify user the error

    :type GatorConnectionError: raises
    :param GatorConnectionError; the error due to information missing are invalid
    :rtype:message
    """
    def __init__(self, email):
        message = f"{email} is already taken. Please try another email."
        super().__init__(message)


class InvalidFormError(GatorConnectionError):
    """
    This class are get the raise and notify user the error

    :type GatorConnectionError: raises
    :param GatorConnectionError; the error due to information missing are invalid
    :rtype:message
    """
    def __init__(self, field, message):
        super().__init__(f"{field} {message}")


class NotVerified(GatorConnectionError):
    """
    This class are get the raise and notify user the error

    :type GatorConnectionError: raises
    :param GatorConnectionError; the error due to information missing are invalid
    :rtype:message
    """
    def __init__(self, message="Your account has not verified yet"):
        super().__init__(message)
