import logging
import yaml
from jinja2 import Template

from database import Database


def execute_worflow(workflow, db):
    return [db.transaction(item) for item in workflow]


def setup_logging(filename):
    FORMAT = '%(asctime)-15s - %(levelname)s - %(module)s - %(message)s'
    logging.basicConfig(filename=filename, level=logging.DEBUG, format=FORMAT)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter(FORMAT)
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def main():
    with open("./Config.yml") as config_file:
        config = yaml.load(config_file)

    setup_logging(config['Logfilename'])

    logging.info('Start Insight Reporting.')

    with open("./workflow.yml") as workflow_file:
        workflow_text = workflow_file.read()
        preprocessed_workflow = Template(workflow_text).render(**config)
        workflow = yaml.load(preprocessed_workflow)

    db = Database(config)
    execute_worflow(workflow, db)

    logging.info('End Insight Reporting.')


if __name__ == '__main__':
    main()
