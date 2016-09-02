import psycopg2


class Database(object):
    def __init__(self, kwargs):
        self.connection = psycopg2.connect(
            "dbname={Database} user={User} password={Password} host={Host} port={Port}".format(**kwargs))
        self.schema_name = kwargs['Schema']

    def transaction(self, item):
        cursor = self.connection.cursor()

        if type(item) is list:
            result = self._execute_transaction(cursor, item)
        else:
            result = self._execute(cursor, item)

        self.connection.commit()
        cursor.close()

        return result

    def _execute_transaction(self, cursor, items):
        result = []
        for item in items:
            result.append(self._execute(cursor, item))

        return result

    def _execute(self, cursor, item):
        cursor.execute(item)

        if cursor.rowcount < 1:
            return []

        return [record for record in cursor]

    def __del__(self):
        self.connection.close()
