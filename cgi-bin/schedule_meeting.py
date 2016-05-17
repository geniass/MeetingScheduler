#!/usr/bin/env python3

import os
from jinja2 import Environment, FileSystemLoader
from db import meeting, meeting_student
import cgi
import cgitb
cgitb.enable()

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, '../templates')),
    trim_blocks=False)

def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

if __name__ == "__main__":
    form = cgi.FieldStorage()
    lecturer_id = form.getfirst("lecturer_id")
    date_time = form.getfirst("date_time")
    student_id = form.getfirst("student_id")
    subject = form.getfirst("subject")
    meeting_detail = form.getfirst("meeting_detail")
    attendees = form.getfirst("attendees")

    updated_meeting = meeting.get_by_date_time(lecturer_id, date_time)
    if updated_meeting:
        updated_meeting.subject = subject
    else:
        updated_meeting = meeting.Meeting(lecturer_id, date_time, 30, subject)

    updated_meeting.save()

    if attendees:
        students = [s.strip() for s in attendees.split(";")]
    else: 
        students = [student_id]

    students_db = meeting_student.get_meeting_attendees(updated_meeting)
    students_to_be_removed = [item for item in students_db if item.student_id not in students]

    for student in students_to_be_removed:
        student.delete()

    for student in students:
        ms = meeting_student.MeetingStudent(updated_meeting,student)
        ms.save()

    print("Content-type: text/html\n")
    html = render_template('schedule_meeting.html', {})
    print(html)
