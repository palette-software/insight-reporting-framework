import logging
import logging.handlers
import yaml
from database import Database
import workflow
import sys

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
    #file_log_handler = logging.RotatingFileHandler(filename=filename, maxBytes=10485760, backupCount=5)
    #file_log_handler = logging.handlers.RotatingFileHandler(filename=filename, maxBytes=100, backupCount=5)
    #file_log_handler.setLevel(logging.DEBUG)
    #formatter = logging.Formatter(FORMAT)
    #file_log_handler.setFormatter(formatter)
    #logging.getLogger('').addHandler(file_log_handler)              

    if console_enabled:        
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        formatter = logging.Formatter(FORMAT)
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

    logging.addLevelName(FATAL_ERROR, 'FATAL')


def main():
    try:
        config_filename = sys.argv[1]
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
