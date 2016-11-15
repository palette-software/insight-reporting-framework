import logging
import psycopg2


class Database(object):
    def __init__(self, kwargs):
        logging.debug("Start creating database connection")
        self.connection = psycopg2.connect(
            "dbname={Database} user={User} password={Password} host={Host} port={Port}".format(**kwargs))
        logging.debug("End creating database connection")
        self.schema_name = kwargs['Schema']

    def execute_multiple_query(self, item):
        if type(item) is list:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    result = self.__execute_all(cursor, item)
        return result

    def execute(self, items):
        for item in items:
            self.execute_single_query(item["name"], item["query"])

    def __execute_all(self, cursor, items):
        result = []
        for item in items:
            result.append(self.__execute(cursor, item["name"], item["query"]))

        return result

    def __execute(self, cursor, name, query):
        logging.info('Start "{}"'.format(name))
        cursor.execute(query)

        if self.__has_no_records(cursor):
            logging.info('End "{}"'.format(name))
            return []

        records = cursor.fetchall()
        logging.info('End "{}" return with: {}'.format(name, records[0][0]))
        return records

    def __has_no_records(self, cursor):
        return cursor.rowcount < 1 or cursor.statusmessage.startswith('DELETE')

    def __del__(self):
        self.connection.close()
        logging.debug("Database connection is closed")

    def execute_single_query(self, name, query):
        with self.connection as connection:
            with connection.cursor() as cursor:
                records =  self.__execute(cursor, name, query)
        return records
