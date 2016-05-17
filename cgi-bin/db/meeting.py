import sqlite3

DB_NAME = "/var/www/development.db"


def get(lecturer_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    args = (lecturer_id,)
    cursor.execute(
        "SELECT ROWID,* FROM meetings WHERE lecturer_id=?", args)

    return [Meeting(lecturer_id, m["datetime"], m['duration'], m["subject"],
                    meeting_id=m["rowid"]) for m in cursor.fetchall()]


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

    return Meeting(lecturer_id, meeting["datetime"], meeting['duration'],
                   meeting["subject"], meeting_id=meeting["rowid"])


def get_all_on(date):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    args = (date,)
    cursor.execute("""SELECT ROWID, * FROM meetings
                   WHERE date(datetime, 'start of day') == date(?, 'start of day')""",
                   args)

    return [Meeting(m["lecturer_id"], m["datetime"], m['duration'], m["subject"],
                    meeting_id=m["rowid"])
            for m in cursor.fetchall()]


class Meeting:

    # duration is in minutes
    def __init__(self, lecturer_id, date_time, duration, subject="",
                 meeting_id=-1):
        self.conn = sqlite3.connect(DB_NAME)
        self.conn.row_factory = sqlite3.Row

        self.meeting_id = meeting_id
        self.lecturer_id = lecturer_id
        self.date_time = date_time
        self.duration = duration
        self.subject = subject

    def save(self):
        cursor = self.conn.cursor()
        meeting = get(self.lecturer_id)
        if meeting:
            # update
            print("update")
            cursor.execute("""UPDATE meetings
                              SET datetime=?, duration=?, subject=?
                              WHERE lecturer_id=?""",
                           (self.date_time, self.duration, self.subject,
                            self.lecturer_id))
        else:
            # insert
            cursor.execute("""INSERT INTO meetings(lecturer_id, datetime, duration, subject)
                              VALUES (?,?,?,?)""",
                           (self.lecturer_id, self.date_time, self.duration,
                            self.subject))

        self.conn.commit()
        return self

    def delete(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM meetings WHERE lecturer_id=?",
                       (self.lecturer_id,))
        self.conn.commit()
        return None
