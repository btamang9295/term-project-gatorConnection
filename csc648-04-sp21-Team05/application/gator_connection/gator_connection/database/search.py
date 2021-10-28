from django.db import connection

from gator_connection.database.sql_builder import SQLBuilder
from gator_connection.database.database import Database


class Search:
    """
    A class that abstracts database interactions to search. Such as convert the input to
    query for retrieving.

    **Methods:**
    - full_text_search(table_name, columns_returned, columns_filtered, search_query)
    - format_query_string(search_query)
    """
    @staticmethod
    def full_text_search(table_name, columns_returned, columns_filtered, search_query):
        """
        This function the get the data from database base on the condition of input.

        :type table_name, search_query: str
        :param table_name, search_query: the elements and the select query
        :type columns_returned, columns_filtered: int
        :param columns_returned, columns_filtered: the elements and the select query
        :return search_results: the data that user want to get in search
        :rtype:list of tuple
        """

        # Filter should be a list of columns that will be searched

        # Columns are the columns that the user wants returned from the search

        sql = SQLBuilder()

        if "all" == search_query:
            sql.select('* FROM {}', [table_name])
        else:
            sql.select(SQLBuilder.build_braces(len(columns_filtered)) + ", ", columns_filtered).match(columns_returned) \
                .against('\'{}\' IN BOOLEAN MODE', [Search.format_query_string(search_query)]) \
                .raw_sql(' AS score FROM {} HAVING score > 0', [table_name]) \
                .order_by('score DESC', [])

        search_results = Database.selectQuery(str(sql))

        return search_results

    @staticmethod
    def format_query_string(search_query):
        """
        This helper function to convert the search string to select query.

        :type search_query: str
        :param search_query: the query to select the data from database
        :rtype:str
        """
        # Split query into array
        split_query = search_query.split()

        # For each word in array add * to front and back
        # ex: test this -> *test* *this*
        final_query = "*" + "* *".join(split_query) + "*"

        return final_query
