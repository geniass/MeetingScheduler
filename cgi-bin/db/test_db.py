import unittest
import os
import sqlite3

import meeting
import meeting_student


class TestDB(unittest.TestCase):

    def setUp(self):
        url = os.getenv("TEST_DB")
        if not url:
            self.skipTest("No database URL set")
        meeting.DB_NAME = url
        meeting_student.DB_NAME = url
        conn = sqlite3.connect(url)
        c = conn.cursor()
        c.execute("DELETE FROM meetings")
        c.execute("INSERT INTO meetings VALUES(2,'2015-01-01',10,'afqweqe')")
        c.execute(
            "INSERT INTO meetings VALUES(3,'2015-01-01T09:00',10,'get a meeting')")

        c.execute("DELETE FROM meetings_students")
        c.execute("INSERT INTO meetings_students VALUES(3, 6878879)")
        c.execute("INSERT INTO meetings_students VALUES(3, 8876767)")

        conn.commit()
        conn.close()

    def test_meeting_save_new_and_update(self):
        m = meeting.Meeting(1, "2015-01-02", 10, "sdvvds")
        self.assertIsNotNone(m.save())

    def test_meeting_get(self):
        m = meeting.get(lecturer_id=3)
        self.assertIsNotNone(m)
        self.assertEqual(m.subject, "get a meeting")

    def test_meeting_get_by_date_time(self):
        m = meeting.get_by_date_time(
            lecturer_id=3, date_time="2015-01-01T09:00")
        self.assertIsNotNone(m)
        self.assertEqual(m.subject, "get a meeting")

    def test_meeting_delete(self):
        m = meeting.get(lecturer_id=2)
        self.assertIsNone(m.delete())
        self.assertIsNone(meeting.get(lecturer_id=2))

    def test_meeting_get_all_on(self):
        ms = meeting.get_all_on("2015-01-01")
        self.assertTrue(len(ms) == 2)

    # MEETING_STUDENT TESTS
    def test_meeting_student_save(self):
        ms = meeting_student.MeetingStudent(3, 985738)
        self.assertIsNotNone(ms.save())

    def test_meeting_student_get(self):
        m = meeting_student.get(3, 8876767)
        self.assertIsNotNone(m)

    def test_meeting_student_get_meeting_attendees(self):
        attendees = meeting_student.get_meeting_attendees(meeting_id=3)
        self.assertEqual(len(attendees), 2)

    def test_meeting_student_delete(self):
        m = meeting_student.get(meeting_id=3, student_id=6878879)
        self.assertIsNone(m.delete())
        self.assertIsNone(meeting_student.get(
            meeting_id=3, student_id=6878879))


if __name__ == '__main__':
    unittest.main()
