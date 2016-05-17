import unittest
import os
import sqlite3

import meeting


class TestDB(unittest.TestCase):

    def setUp(self):
        url = os.getenv("TEST_DB")
        if not url:
            self.skipTest("No database URL set")
        meeting.DB_NAME = url
        conn = sqlite3.connect(url)
        c = conn.cursor()
        c.execute("DELETE FROM meetings")
        c.execute("INSERT INTO meetings VALUES(2,'2015-01-01',10,'afqweqe')")
        c.execute(
            "INSERT INTO meetings VALUES(3,'2015-01-01T09:00',10,'get a meeting')")
        conn.commit()
        conn.close()

    def test_save_new_and_update(self):
        m = meeting.Meeting(1, "2015-01-02", 10, "sdvvds")
        self.assertIsNotNone(m.save())

    def test_get_a_meeting(self):
        m = meeting.get(lecturer_id=3)
        self.assertIsNotNone(m)
        self.assertEqual(m.subject, "get a meeting")

    def test_get_by_date_time(self):
        m = meeting.get_by_date_time(
            lecturer_id=3, date_time="2015-01-01T09:00")
        self.assertIsNotNone(m)
        self.assertEqual(m.subject, "get a meeting")

    def test_delete(self):
        m = meeting.get(lecturer_id=2)
        self.assertIsNone(m.delete())
        self.assertIsNone(meeting.get(lecturer_id=2))

    def test_get_all_on(self):
        ms = meeting.get_all_on("2015-01-01")
        self.assertTrue(len(ms) == 2)


if __name__ == '__main__':
    unittest.main()
