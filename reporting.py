import logging
import pprint

import yaml
from jinja2 import Template

from database import Database


def execute_worflow(workflow, db):
    return [db.transaction(item) for item in workflow]


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
        workflow_text = workflow_file.read()
        preprocessed_workflow = Template(workflow_text).render(**config)
        workflow = yaml.load(preprocessed_workflow)

    db = Database(config)
    result = execute_worflow(workflow, db)
    pprint.pprint(result, indent=2)

    logging.info('End Insight Reporting.')


if __name__ == '__main__':
    main()
