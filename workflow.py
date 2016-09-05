TRANSACTION = 'transaction'
QUERIES = 'queries'
NAME = 'name'


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
