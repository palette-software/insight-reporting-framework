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
