#!/usr/bin/env python3

import os
from jinja2 import Environment, FileSystemLoader
from db import meeting, meeting_student
import cgi
import cgitb
cgitb.enable()


def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False


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
    is_group_booking = str_to_bool(form.getfirst("group_booking", "False"))
    is_student_booking = str_to_bool(form.getfirst("student_booking", "False"))
    attendees = form.getfirst("attendees", "")

    updated_meeting = meeting.get_by_date_time(lecturer_id, date_time)
    if updated_meeting:
        updated_meeting.subject = subject
    else:
        updated_meeting = meeting.Meeting(lecturer_id, date_time, 30, subject)
    updated_meeting.is_group_meeting = is_group_booking

    updated_meeting.save()

    # if its a group meeting, allow multiple attendees
    # else only look at the student id
    if is_group_booking and not is_student_booking:
        students = [s.strip() for s in attendees.split(";")]
    else:
        students = [student_id] if student_id else []

    if is_group_booking and not is_student_booking:
        # remove students who are no longer in the list of attendees but are still
        # in the database
        students_db = meeting_student.get_meeting_attendees(updated_meeting)
        students_to_be_removed = [
            item for item in students_db if item.student_id not in students]

        for student in students_to_be_removed:
            student.delete()

    for student in students:
        ms = meeting_student.MeetingStudent(updated_meeting, student)
        ms.save()

    print("Content-type: text/html\n")
    html = render_template('schedule_meeting.html', {})
    print(html)
