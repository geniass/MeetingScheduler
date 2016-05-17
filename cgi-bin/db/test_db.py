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
        c.execute("INSERT INTO meetings VALUES(3,'2014-01-01',10,'afqweqe')")
        c.execute(
            "INSERT INTO meetings VALUES(3,'2015-01-01T09:00',10,'get a meeting')")
        c.execute(
            "INSERT INTO meetings VALUES(3,'2015-01-01',10,'another meeting')")

        c.execute("DELETE FROM meetings_students")
        c.execute("INSERT INTO meetings_students VALUES(2, 6878879)")
        c.execute("INSERT INTO meetings_students VALUES(2, 8876767)")

        conn.commit()
        conn.close()

    def test_meeting_save_new_and_update(self):
        m = meeting.Meeting(1, "2015-01-02", 10, "sdvvds")
        self.assertIsNotNone(m.save())

    def test_meeting_get_for_lecturer(self):
        ms = meeting.get(lecturer_id=3)
        self.assertEqual(len(ms), 3)

    def test_meeting_get_by_date_time(self):
        m = meeting.get_by_date_time(
            lecturer_id=3, date_time="2015-01-01T09:00")
        self.assertIsNotNone(m)
        self.assertEqual(m.subject, "get a meeting")

    def test_meeting_delete(self):
        m = meeting.get_by_date_time(3, '2014-01-01')
        self.assertIsNone(m.delete())
        self.assertIsNone(meeting.get_by_date_time(3, '2014-01-01'))

    def test_meeting_get_all_on(self):
        ms = meeting.get_all_on("2015-01-01")
        self.assertEqual(len(ms), 2)

    # MEETING_STUDENT TESTS
    def test_meeting_student_save(self):
        m = meeting.Meeting(3, '2015-01-01T09:00', 10)
        ms = meeting_student.MeetingStudent(m, 985738)
        self.assertIsNotNone(ms.save())

    def test_meeting_student_get(self):
        m = meeting.Meeting(3, '2015-01-01T09:00', 10)
        ms = meeting_student.get(m, 8876767)
        self.assertIsNotNone(ms)

    def test_meeting_student_get_meeting_attendees(self):
        m = meeting.Meeting(3, '2015-01-01T09:00', 10)
        attendees = meeting_student.get_meeting_attendees(m)
        self.assertEqual(len(attendees), 2)

    def test_meeting_student_delete(self):
        m = meeting.Meeting(3, '2015-01-01T09:00', 10)
        ms = meeting_student.get(m, 6878879)
        self.assertIsNone(ms.delete())
        self.assertIsNone(meeting_student.get(m, 6878879))


if __name__ == '__main__':
    unittest.main()
