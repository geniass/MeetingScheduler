import meeting
import sqlite3

DB_NAME = "/var/www/development.db"


def get(meeting_row, student_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if meeting_row.meeting_id == -1:
        meeting_row = meeting.get_by_date_time(
            meeting_row.lecturer_id, meeting_row.date_time)

    args = (meeting_row.meeting_id, student_id)
    cursor.execute(
        "SELECT * FROM meetings_students WHERE meeting_id=? AND student_id=?", args)
    meeting_student = cursor.fetchone()

    if not meeting_student:
        return None

    return MeetingStudent(meeting_row, meeting_student['student_id'])


def get_meeting_attendees(meeting_row):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if meeting_row.meeting_id == -1:
        meeting_row = meeting.get_by_date_time(
            meeting_row.lecturer_id, meeting_row.date_time)

    args = (meeting_row.meeting_id,)
    cursor.execute(
        "SELECT * FROM meetings_students WHERE meeting_id=?", args)

    return [MeetingStudent(meeting_row, m['student_id']) for m in cursor.fetchall()]


class MeetingStudent:

    def __init__(self, meeting_row, student_id):
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = sqlite3.Row

        if meeting_row.meeting_id == -1:
            # meeting_row hasn't been queried in the db, so do that now to find
            # its meeting_id
            self.meeting = meeting.get_by_date_time(
                meeting_row.lecturer_id, meeting_row.date_time)
        else:
            self.meeting = meeting_row

        self.student_id = student_id

    def save(self):
        cursor = self.conn.cursor()
        # insert
        cursor.execute("""INSERT INTO meetings_students(meeting_id,student_id)
                            VALUES (?,?)""",
                       (self.meeting.meeting_id, self.student_id))

        self.conn.commit()
        return self

    def delete(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM meetings_students WHERE meeting_id=? AND student_id=?",
                       (self.meeting.meeting_id, self.student_id))
        self.conn.commit()
        return None
