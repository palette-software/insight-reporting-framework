import unittest

import workflow


class WorkflowTest(unittest.TestCase):
    def setUp(self):
        self.item_wo_transaction = {
            "name": "Test",
            "queries": "select",
        }

        self.item_with_transaction = {
            "name": "Test",
            "queries": "select",
            "transaction": True
        }

    def test_validate_None(self):
        self.assertFalse(workflow.validate(None))

    def test_validate_empty_list(self):
        self.assertTrue(workflow.validate([]))

    def test_validate_item_is_not_empty_dict(self):
        self.assertFalse(workflow.validate_item({}))

    def test_validate_item_has_all_attribute(self):
        self.assertTrue(workflow.validate_item(self.item_with_transaction))

    def test_validate_item_transaction_is_bool(self):
        item = {
            "name": "Test",
            "queries": "select",
            "transaction": 'True'
        }
        self.assertFalse(workflow.validate_item(item))

    def test_validate_item_transaction_is_optional(self):
        self.assertTrue(workflow.validate_item(self.item_wo_transaction))

    def test_is_transaction_is_optional(self):
        self.assertFalse(workflow.is_transaction(self.item_wo_transaction))

    def test_is_transaction_true(self):
        self.assertTrue(workflow.is_transaction(self.item_with_transaction))

    def test_is_transaction_false(self):
        item = {
            "name": "Test",
            "queries": "select",
            "transaction": False
        }
        self.assertFalse(workflow.is_transaction(item))
