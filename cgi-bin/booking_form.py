#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
from db import meeting
import cgi
import cgitb
cgitb.enable()


def populate_template(lecturer_id, date_time, subject="", is_student_booking=False, is_group_booking=False, attendees=["547937", "597609"]):
    loader = FileSystemLoader('../templates')
    env = Environment(loader=loader)

    context = {"lecturer_id": lecturer_id,
               "date_time": date_time, "subject": subject, "is_group_booking": is_group_booking, "attendees": attendees}
    return env.get_template("booking_form.html").render(context)

if __name__ == "__main__":
    form = cgi.FieldStorage()
    lecturer_id = form.getfirst("lecturer_id")
    date_time = form.getfirst("date_time")

    # need to fix lecture_id and date_time to not crash if does not exist
    m = meeting.get_by_date_time(lecturer_id, date_time)

    ################!!!!!!!! TO DO !!!!!!!!!!!!!!!! ##########################
    # Need to read from the database to get the students who have booked and
    # therefore whether it is a group meeting

    print("Content-type: text/html\n")
    print(populate_template(lecturer_id, date_time, subject=m.subject))
