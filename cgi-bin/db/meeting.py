import sqlite3

DB_NAME = "/var/www/development.db"


def get(lecturer_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    args = (lecturer_id,)
    cursor.execute(
        "SELECT ROWID,* FROM meetings WHERE lecturer_id=?", args)

    return [from_meeting_row(m) for m in cursor.fetchall()]


def get_by_date_time(lecturer_id, date_time):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    args = (lecturer_id, date_time)
    cursor.execute(
        "SELECT ROWID,* FROM meetings WHERE lecturer_id=? AND datetime=?",
        args)
    meeting = cursor.fetchone()

    if not meeting:
        return None

    return from_meeting_row(meeting)


def get_all_on(lecturer_id, date):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    args = (lecturer_id, date)
    cursor.execute(
        "SELECT ROWID,* FROM meetings WHERE lecturer_id=? AND date(datetime,'start of day') == date(?,'start of day')", args)

    return [from_meeting_row(m) for m in cursor.fetchall()]


def from_meeting_row(row):
    is_group_meeting = True if row['is_group_meeting'] == 1 else False
    return Meeting(row['lecturer_id'], row['datetime'], row['duration'],
                   row['subject'], meeting_id=row['rowid'],
                   is_group_meeting=is_group_meeting)


class Meeting:

    # duration is in minutes
    def __init__(self, lecturer_id, date_time, duration, subject="",
                 meeting_id=-1, is_group_meeting=False):
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = sqlite3.Row

        self.meeting_id = meeting_id
        self.lecturer_id = lecturer_id
        self.date_time = date_time
        self.duration = duration
        self.subject = subject
        self.is_group_meeting = is_group_meeting

    def save(self):
        cursor = self.conn.cursor()
        meeting = get_by_date_time(self.lecturer_id, self.date_time)
        if meeting:
            # update
            cursor.execute("""UPDATE meetings
                              SET datetime=?,duration=?,subject=?,is_group_meeting=?
                              WHERE lecturer_id=?""",
                           (self.date_time, self.duration, self.subject,
                            0 if not self.is_group_meeting else 1,
                            self.lecturer_id))
        else:
            # insert
            cursor.execute("""INSERT INTO meetings(lecturer_id, datetime, duration, 
                              subject, is_group_meeting)
                              VALUES (?,?,?,?,?)""",
                           (self.lecturer_id, self.date_time, self.duration,
                            self.subject, 0 if not self.is_group_meeting else 1))

        self.conn.commit()
        return self

    def delete(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM meetings WHERE lecturer_id=?",
                       (self.lecturer_id,))
        self.conn.commit()
        return None
