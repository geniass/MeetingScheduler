#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import cgi
import cgitb
cgitb.enable()

# change permissions of this file to run

def populate_template(lecturer_id, date_time, is_student_booking=False):
    loader = FileSystemLoader('../templates')
    env = Environment(loader=loader)

    context = {"lecturer_id": lecturer_id,
               "date_time": date_time, "subject": "sdfsf"}
    return env.get_template("booking_form.html").render(context)

if __name__ == "__main__":
    form = cgi.FieldStorage()
    lecturer_id = form.getfirst("lecturer_id")
    date_time = form.getfirst("date_time")

    print("Content-type: text/html\n")
    print(populate_template(lecturer_id, date_time))
