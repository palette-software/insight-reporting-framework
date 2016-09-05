import unittest
from unittest.mock import MagicMock

import reporting
import workflow


class ReportingTest(unittest.TestCase):

    def test_execute_workflow(self):
        config = reporting.load_config('Config.yml')
        tasks = workflow.load_from_file('workflow.yml', config)

        db = MagicMock()

        reporting.execute_workflow(tasks, db)

        self.assertEqual(2, db.execute.call_count)
        self.assertEqual(1, db.execute_in_transaction.call_count)
