import unittest
from unittest import mock

import reporting
import workflow


class ReportingTest(unittest.TestCase):

    def test_execute_workflow(self):
        config = reporting.load_config('Config.yml')
        tasks = workflow.load_from_file('workflow.yml', config)

        db = mock.MagicMock()

        reporting.execute_workflow(tasks, db)

        db.execute.assert_has_calls([mock.call(tasks[0]['queries']), mock.call(tasks[2]['queries'])])
        db.execute_in_transaction.assert_called_once_with(tasks[1]['queries'])
