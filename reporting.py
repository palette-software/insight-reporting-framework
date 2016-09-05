import logging
import yaml
from jinja2 import Template

from database import Database

FATAL_ERROR = 49


def execute_workflow(workflow, db):
    for item in workflow:
        logging.info('Start "{}"'.format(item['name']))
        if item.get('transaction', False):
            db.execute_in_transaction(item['queries'])
        else:
            db.execute(item['queries'])
        logging.info('End "{}"'.format(item['name']))


def setup_logging(filename):
    FORMAT = '%(asctime)-15s - %(levelname)-5s - %(module)-10s - %(message)s'
    logging.basicConfig(filename=filename, level=logging.DEBUG, format=FORMAT)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(FORMAT)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.addLevelName(FATAL_ERROR, 'FATAL')


def main():
    try:
        with open("./Config.yml") as config_file:
            config = yaml.load(config_file)

        setup_logging(config['Logfilename'])

        logging.info('Start Insight Reporting.')

        workflow_filename = config['WorkflowFilename']
        with open(workflow_filename) as workflow_file:
            workflow_text = workflow_file.read()
            preprocessed_workflow = Template(workflow_text).render(**config)
            workflow = yaml.load(preprocessed_workflow)

        db = Database(config)
        logging.debug('Executing "{}" workflow'.format(workflow_filename))
        execute_workflow(workflow, db)

        logging.info('End Insight Reporting.')
    except Exception as exception:
        logging.log(FATAL_ERROR, 'Unhandled exception occurred: {}'.format(exception))

if __name__ == '__main__':
    main()
