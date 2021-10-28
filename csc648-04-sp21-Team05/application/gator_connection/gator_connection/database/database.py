from datetime import datetime

from django.db import connection


class Database:
    """
    A class that abstracts database operating. Such for get Time, Query.

    **Methods:**
    - getTimeNow()
    - selectQuery(sql)
    - insertQuery(sql)

    """
    @staticmethod
    def getTimeNow():
        """
        This function are get the time and format that.
        :return:string time
        :rtype:str
        """
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @staticmethod
    def selectQuery(sql):
        """
        This function are get the list of tuple from database.

        :type sql: str
        :param sql: Should be a command for database
        :return:None or list
        :rtype:list of tuples
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)

            return Database.__dict_fetch_all(cursor)

    @staticmethod
    def insertQuery(sql):
        """
        This function are insert the list of tuple to database.

        :type sql: str
        :param sql: Should be a command for database
        :return:None or list
        :rtype:list of tuples
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)

            return cursor

    @staticmethod
    def __dict_fetch_all(cursor):
        if cursor.description == None:
            return None

        columns = [col[0] for col in cursor.description]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
