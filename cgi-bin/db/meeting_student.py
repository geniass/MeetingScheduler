import sqlite3

DB_NAME = "/var/www/development.db"


def get(meeting_id, student_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    args = (meeting_id, student_id)
    cursor.execute(
        "SELECT * FROM meetings_students WHERE meeting_id=? AND student_id=?", args)
    meeting_student = cursor.fetchone()

    if not meeting_student:
        return None

    return MeetingStudent(meeting_student['meeting_id'], meeting_student['student_id'])


def get_meeting_attendees(meeting_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    args = (meeting_id,)
    cursor.execute(
        "SELECT * FROM meetings_students WHERE meeting_id=?", args)

    return [MeetingStudent(m['meeting_id'], m['student_id']) for m in cursor.fetchall()]


class MeetingStudent:

    def __init__(self, meeting_id, student_id):
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = sqlite3.Row

        self.meeting_id = meeting_id
        self.student_id = student_id

    def save(self):
        cursor = self.conn.cursor()
        # insert
        print("insert")
        cursor.execute("""INSERT INTO meetings_students(meeting_id,student_id)
                            VALUES (?,?)""",
                       (self.meeting_id, self.student_id))

        self.conn.commit()
        return self

    def delete(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM meetings_students WHERE meeting_id=? AND student_id=?",
                       (self.meeting_id, self.student_id))
        self.conn.commit()
        return None
