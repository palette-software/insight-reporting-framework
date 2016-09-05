import yaml
from jinja2 import Template

TRANSACTION = 'transaction'
QUERIES = 'queries'
NAME = 'name'


def load(filename, config):
    with open(filename) as workflow_file:
        workflow_text = workflow_file.read()
        preprocessed_workflow = Template(workflow_text).render(**config)
        workflow = yaml.load(preprocessed_workflow)
    return workflow


def validate(workflow):
    if type(workflow) is not list:
        return False
    return True


def validate_item(item):
    if type(item) is not dict:
        return False
    if NAME not in item:
        return False
    if QUERIES not in item:
        return False
    if TRANSACTION in item and type(item[TRANSACTION]) is not bool:
        return False

    return True


def is_transaction(item):
    validate_item(item)
    return item.get(TRANSACTION, False)
