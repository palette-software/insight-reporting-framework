import unittest
import yaml

class ReportingTest(unittest.TestCase):

    def setUp(self):
        self.config = yaml.load(\
"""Host: dev-insight.palette-software.net
Port: 5432
User: palette_etl_user
Password: palette123
Database: palette
Schema: palette
""")

        with open("./workflow.yml") as workflow_file:
            self.workflow = yaml.load(workflow_file)

    def tearDown(self):
        pass

    def test_config_has_all_items(self):
        self.assertEqual(6, len(self.config))


