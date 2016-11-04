import logging
import psycopg2


class Database(object):
    def __init__(self, kwargs):
        logging.debug("Start creating database connection")
        self.connection = psycopg2.connect(
            "dbname={Database} user={User} password={Password} host={Host} port={Port}".format(**kwargs))
        logging.debug("End creating database connection")
        self.schema_name = kwargs['Schema']

    def execute_in_transaction(self, item):
        with self.connection as connection:
            with connection.cursor() as cursor:
                if type(item) is list:
                    result = self.__execute_all(cursor, item)
                else:
                    result = self.__execute(cursor, item)
        return result

    def execute(self, items):
        for item in items:
            self.execute_in_transaction(item)

    def __execute_all(self, cursor, items):
        result = []
        for item in items:
            result.append(self.__execute(cursor, item))

        return result

    def __execute(self, cursor, item):
        logging.info('Start "{}"'.format(item['name']))
        cursor.execute(item['query'])

        if self.__has_no_records(cursor):
            logging.info('End "{}"'.format(item['name']))
            return []

        records = cursor.fetchall()
        logging.info('End "{}" return with: {}'.format(item['name'], records[0][0]))
        return records

    def __has_no_records(self, cursor):
        return cursor.rowcount < 1 or cursor.statusmessage.startswith('DELETE')

    def __del__(self):
        self.connection.close()
        logging.debug("Database connection is closed")

    def execute_single_query(self, query):
        with self.connection as connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                records = cursor.fetchall()
        return records
