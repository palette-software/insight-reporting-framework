import unittest
import yaml
import reporting


class ReportingTest(unittest.TestCase):
    def setUp(self):
        self.config = yaml.load(\
"""
Host: dev-insight.palette-software.net
Port: 5432
User: palette_etl_user
Password: palette123
Database: palette
Schema: palette
""")

        self.workflow = yaml.load(\
"""
- test_py(#schema_name#)
-
  - test_py(#schema_name#)
  - test_py(#schema_name#)
  - test_py(#schema_name#)
- test_py(#schema_name#)
""")

    def tearDown(self):
        pass

    def test_config_has_all_items(self):
        self.assertEqual(6, len(self.config))

    def test_preprocess_one_item(self):
        wf = reporting.preprocess_workflow(self.workflow, self.config)
        self.assertIsInstance(wf[0], str)

    def test_preprocess_multiple_item(self):
        wf = reporting.preprocess_workflow(self.workflow, self.config)
        self.assertIsInstance(wf[1], list)
        self.assertEqual(len(wf[1]), 3)
