import logging
import psycopg2
import yaml


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


def execute_worflow(workflow, config):
    db = Database(config)

    for item in workflow:
        result = db.transaction(item)
        print(result)


def preprocess_workflow(workflow, config):
    schema_name = config["Schema"]
    new_workflow = []
    for item in workflow:
        if type(item) is list:
            new_item = preprocess_workflow(item, config)
        else:
            new_item = item.replace("#schema_name#", "'" + schema_name + "'")
        new_workflow.append(new_item)
    return new_workflow


def main():
    logging.basicConfig(filename='./insight-reporting.log', level=logging.DEBUG)
    logging.info('Start Insight Reporting.')

    with open("./Config.yml") as config_file:
        config = yaml.load(config_file)

    with open("./workflow.yml") as workflow_file:
        workflow = yaml.load(workflow_file)

    preprocessed_workflow = preprocess_workflow(workflow, config)
    execute_worflow(preprocessed_workflow, config)

    logging.info('End Insight Reporting.')


if __name__ == '__main__':
    main()
