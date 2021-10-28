class SQLBuilder:
    """Build basic SQL queries using this class.\n NOTE: All SQL queries returned will not have a ";" appended. Therefore,
    must call str(SQLBuilder) and will automatically append ";".
    """

    @staticmethod
    def build_braces(length):
        """Builds a comma separated list of {}'s based off the length.
                ex: SQLBuilder.buildBraces(3)
                    returns "{}, {}, {}"
        """
        result = ''
        for i in range(length):
            result += '{}'

            if i + 1 < length:
                result += ', '
        return result

    def __init__(self):
        self.__sql = ''

    def select(self, string, values=None):
        """Build basic SELECT SQL query.\n Keyword arguments: string -- String parameter that should have correct SQL
        syntax with values replaced with {} not including SELECT

        values -- List of strings parameter of values that will fill in {} positions in sql string in the order
        given

            ex: select("{}, {}, {} FROM {}", ["first_name", "last_name", "email", "student"])
                adds "SELECT first_name, last_name, email FROM student"

        returns -- self, so can chain methods
        """
        self.__sql += ' SELECT ' + self.__format_sql(string, values)
        return self

    def where(self, string, values=None):
        """Build basic WHERE SQL query.\n Keyword arguments: string -- String parameter that should have correct SQL
        syntax with values replaced with {} not including WHERE

        values -- List of strings parameter of values that will fill in {} positions in sql string in the order given

            ex: where("{} > {}", ["age", 5])
                adds "WHERE age > 5"

        returns -- self, so can chain methods
        """
        self.__sql += ' WHERE ' + self.__format_sql(string, values)
        return self

    def order_by(self, string, values=None):
        self.__sql += ' ORDER BY ' + self.__format_sql(string, values)
        return self

    def insert(self, string, values=None):
        self.__sql += ' INSERT ' + self.__format_sql(string, values)
        return self

    def update(self, string, values=None):
        self.__sql += ' UPDATE ' + self.__format_sql(string, values)
        return self

    def delete(self, string, values=None):
        self.__sql += ' DELETE ' + self.__format_sql(string, values)
        return self

    def match(self, values=None):
        self.__sql += ' MATCH(' + ', '.join(values) + ")"
        return self

    def against(self, string, values=None):
        self.__sql += ' AGAINST(' + self.__format_sql(string, values) + ")"
        return self

    def raw_sql(self, string, values=None):
        self.__sql += self.__format_sql(string, values)
        return self

    def __format_sql(self, string, values):

        if values is None or len(values) < 1:
            return string

        requested_num_of_variables = string.count('{}')

        if not (requested_num_of_variables == len(values)):
            raise ValueError("Number of {}'s in string parameter must be equal to number of values in values list")

        return string.format(*values)

    def __str__(self):
        return self.__sql + ";"
