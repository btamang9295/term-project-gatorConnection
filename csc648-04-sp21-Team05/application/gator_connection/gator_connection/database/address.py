from gator_connection.database.gator_connection_exceptions import *


class Address:
    """
    A class that check the validation of information from Address form.

    **Methods:**
    - validateAddress(zipcode, number, street, city)

    """
    @staticmethod
    def validateAddress(zipcode, number, street, city):
        """
        :param zipcode, number, street, city:The data from the Address form
        :type zipcode, number: int
        :type street, city: str
        :raise: ValueError: the data is cannot pass the validation cause data type or length
        """

        # Check if zipcode is a number
        try:
            zipcode_int = int(zipcode)
        except ValueError:
            raise InvalidFormError(zipcode, "is not a zip code, should be a 5 digit number")

        # Check if zipcode is 5 digits long
        zipcode_length = len(zipcode)

        if zipcode_length != 5:
            raise InvalidFormError(zipcode, "is not a valid zip code. Zip codes are 5 digits long.")

        # Check if number is a number
        try:
            number_int = int(number)
        except ValueError:
            raise InvalidFormError(number, "is not a valid street number.")

        # Check if street will fit in database

        street_length = len(street)

        if street_length > 90:
            raise InvalidFormError(street,
                                   f"is too long of a street name, please abbreviate it. Max number of characters "
                                   f"allowed is 90. Current Length: {street_length}")

        # Check if city will fit in database
        city_length = len(city)

        if city_length > 90:
            raise InvalidFormError(city, f"is too long of a city name, please abbreviate it. Max number of characters "
                                         f"allowed is 90. Current Length: {city_length}")
