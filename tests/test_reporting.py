import unittest
import datetime
from unittest import mock

from database import Database
import reporting
import workflow

class ReportingTest(unittest.TestCase):

    @mock.patch("psycopg2.connect")
    def test_last_loaded_day(self, mock_connect):
        expected = [['1001-01-01']]

        mock_con = mock_connect.return_value.__enter__.return_value  # result of psycopg2.connect(**connection_stuff)
        mock_cur = mock_con.cursor.return_value.__enter__.return_value  # result of con.cursor(cursor_factory=DictCursor)
        mock_cur.fetchall.return_value = expected  # return this when calling cur.fetchall()
        mock_cur.rowcount = len(expected)
        mock_cur.statusmessage = ""

        db = Database({"Database": "fake", "User": "fake", "Password": "Fake", "Host": "Fake", "Port": 1, "Schema": "Fake"})


        self.assertEqual(reporting.get_last_loaded_day(db, 'palette'), '1001-01-01')

    @mock.patch("workflow.load_from_file")
    @mock.patch("reporting.get_next_day")
    @mock.patch("reporting.get_last_loadable_day")
    @mock.patch("reporting.get_last_loaded_day")
    @mock.patch("psycopg2.connect")
    def test_load_days(self, mock_connect, mock_last_loaded_day, mock_last_loadable_day, mock_get_next_day, mock_load_from_file):
        mock_get_next_day.return_value = datetime.date(2016, 11, 11)
        mock_last_loadable_day.return_value = datetime.date(2016, 11, 13)
        mock_last_loaded_day.return_value = datetime.date(1001, 1, 1)
        db = Database({"Database": "fake", "User": "fake", "Password": "Fake", "Host": "Fake", "Port": 1, "Schema": "Fake"})

        reporting.load_days(db, {"Schema": "Fake"}, "path/to/workflow")
        mock_load_from_file.assert_any_call("path/to/workflow", {"Schema": "Fake"}, datetime.date(2016, 11, 11))
        mock_load_from_file.assert_any_call("path/to/workflow", {"Schema": "Fake"}, datetime.date(2016, 11, 12))
        mock_load_from_file.assert_any_call("path/to/workflow", {"Schema": "Fake"}, datetime.date(2016, 11, 13))
        with self.assertRaises(AssertionError):
            mock_load_from_file.assert_any_call("path/to/workflow", {"Schema": "Fake"}, datetime.date(2016, 11, 14))
        with self.assertRaises(AssertionError):
            mock_load_from_file.assert_any_call("path/to/workflow", {"Schema": "Fake"}, datetime.date(2016, 11, 10))

    @mock.patch("workflow.load_from_file")
    @mock.patch("reporting.get_next_day")
    @mock.patch("reporting.get_last_loadable_day")
    @mock.patch("reporting.get_last_loaded_day")
    @mock.patch("psycopg2.connect")
    def test_load_days_today_not_possible(self, mock_connect, mock_last_loaded_day, mock_last_loadable_day, mock_get_next_day, mock_load_from_file):
        mock_get_next_day.return_value = datetime.date(2016, 11, 12)
        mock_last_loadable_day.return_value = datetime.date(2016, 11, 13)
        mock_last_loaded_day.return_value = datetime.date(2016, 11, 11)
        db = Database({"Database": "fake", "User": "fake", "Password": "Fake", "Host": "Fake", "Port": 1, "Schema": "Fake"})

        reporting.load_days(db, {"Schema": "Fake"}, "path/to/workflow")
        mock_load_from_file.assert_any_call("path/to/workflow", {"Schema": "Fake"}, datetime.date(2016, 11, 12))
        mock_load_from_file.assert_any_call("path/to/workflow", {"Schema": "Fake"}, datetime.date(2016, 11, 13))
        with self.assertRaises(AssertionError):
            mock_load_from_file.assert_any_call("path/to/workflow", {"Schema": "Fake"}, datetime.date(2016, 11, 14))
        with self.assertRaises(AssertionError):
            mock_load_from_file.assert_any_call("path/to/workflow", {"Schema": "Fake"}, datetime.date(2016, 11, 11))

    @mock.patch("workflow.load_from_file")
    @mock.patch("reporting.get_next_day")
    @mock.patch("reporting.get_last_loadable_day")
    @mock.patch("reporting.get_last_loaded_day")
    @mock.patch("psycopg2.connect")
    def test_load_days_normal(self, mock_connect, mock_last_loaded_day, mock_last_loadable_day, mock_get_next_day, mock_load_from_file):
        mock_get_next_day.return_value = datetime.date(2016, 11, 14)
        mock_last_loadable_day.return_value = datetime.date(2016, 11, 13)
        mock_last_loaded_day.return_value = datetime.date(2016, 11, 13)
        db = Database({"Database": "fake", "User": "fake", "Password": "Fake", "Host": "Fake", "Port": 1, "Schema": "Fake"})

        reporting.load_days(db, {"Schema": "Fake"}, "path/to/workflow")
        with self.assertRaises(AssertionError):
            mock_load_from_file.assert_any_call("path/to/workflow", {"Schema": "Fake"}, datetime.date(2016, 11, 13))
        with self.assertRaises(AssertionError):
            mock_load_from_file.assert_any_call("path/to/workflow", {"Schema": "Fake"}, datetime.date(2016, 11, 14))
        mock_load_from_file.assert_not_called()





