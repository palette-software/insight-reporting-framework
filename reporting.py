import logging

import yaml

from database import Database
import workflow

FATAL_ERROR = 49


def execute_workflow(workflow, db):
    for item in workflow:
        logging.info('Start "{}"'.format(item['name']))
        if item.get('transaction', False):
            db.execute_in_transaction(item['queries'])
        else:
            db.execute(item['queries'])
        logging.info('End "{}"'.format(item['name']))


def load_config(filename):
    with open(filename) as config_file:
        config = yaml.load(config_file)
    return config


def setup_logging(filename, console_enabled):
    FORMAT = '%(asctime)-15s - %(levelname)-5s - %(module)-10s - %(message)s'
    logging.basicConfig(filename=filename, level=logging.DEBUG, format=FORMAT)
    
    if console_enabled:        
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter(FORMAT)
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    logging.addLevelName(FATAL_ERROR, 'FATAL')


def main():
    try:
        config_filename = "./Config.yml"
        config = load_config(config_filename)

        setup_logging(config['Logfilename'], config['ConsoleLog'])

        logging.info('Start Insight Reporting.')

        workflow_filename = config['WorkflowFilename']
        workflow_doc = workflow.load_from_file(workflow_filename, config)

        db = Database(config)
        logging.debug('Executing "{}" workflow'.format(workflow_filename))
        execute_workflow(workflow_doc, db)

        logging.info('End Insight Reporting.')
    except Exception as exception:
        logging.log(FATAL_ERROR, 'Unhandled exception occurred: {}'.format(exception))


if __name__ == '__main__':
    main()
