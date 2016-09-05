import logging
import psycopg2


class Database(object):
    def __init__(self, kwargs):
        logging.debug("Start database connection")
        self.connection = psycopg2.connect(
            "dbname={Database} user={User} password={Password} host={Host} port={Port}".format(**kwargs))
        logging.debug("End database connection")
        self.schema_name = kwargs['Schema']

    def transaction(self, item):
        with self.connection as connection:
            with connection.cursor() as cursor:
                if type(item) is list:
                    result = self._execute_transaction(cursor, item)
                else:
                    result = self._execute(cursor, item)
        return result

    def _execute_transaction(self, cursor, items):
        result = []
        for item in items:
            result.append(self._execute(cursor, item))

        return result

    def _execute(self, cursor, item):
        logging.info('Start "{}"'.format(item['name']))
        cursor.execute(item['query'])

        if cursor.rowcount < 1:
            logging.info('End "{}"'.format(item['name']))
            return []

        records = cursor.fetchall()
        logging.info('End "{}" return with: {}'.format(item['name'], records[0][0]))
        return records

    def __del__(self):
        self.connection.close()
        logging.debug("Database connection is closed")

