#!/usr/bin/env python3

from db import meeting
import os
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
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


def frange(x, y, jump):
    while x < y:
        yield x
        x += jump


def requested_date(given_date):
    date = datetime.strptime(given_date, "%Y-%m-%d")
    days = [date.date()]
    for i in range(1, 7):
        date2 = date + timedelta(days=i)
        days.append(date2.date())
    return days


def create_index_html(lecturer_id, startDate, is_student_booking=True):
    days = requested_date(startDate)

    weekly_data = dict()
    for day in days:
        weekly_data[day] = []
        meetings = meeting.get_all_on(lecturer_id, day)
        time = datetime.strptime("08:00", "%H:%M")
        for k in range(18):
            slot_meeting = None
            for m in meetings:
                m_date = datetime.strptime(
                    m.date_time, "%Y-%m-%dT%H:%M")
                m_time = m_date.time().replace(second=0)
                if m_time == time.time():
                    slot_meeting = m
                    break

                ####### TODO ########
                # get group booking from db

            link_str = ("/cgi-bin/booking_form.py?"
                        "lecturer_id={0}&"
                        "date_time={1}&"
                        "student_booking={2}&"
                        "group_booking={3}")
            if not slot_meeting:
                # not busy
                weekly_data[day].append({'status': 'Book',
                                         'link': link_str.format(
                                             lecturer_id,
                                             datetime.combine(day, time.time())
                                             .strftime("%Y-%m-%dT%H:%M"),
                                             is_student_booking,
                                             False)})
            else:
                if is_student_booking:
                    # don't show edit
                    weekly_data[day].append({'status': 'Busy', 'link': ''})
                else:
                    # show edit
                    weekly_data[day].append({'status': 'Edit',
                                             'link': link_str.format(
                                                 lecturer_id,
                                                 datetime.combine(
                                                     day, time.time())
                                                 .strftime("%Y-%m-%dT%H:%M"),
                                                 is_student_booking,
                                                 False)})

            slot = time.strftime("%H:%M")
            time = time + timedelta(minutes=30)

    time_slot = datetime.strptime("08:00", "%H:%M")
    time = []
    for k in range(18):
        slot = time_slot.strftime("%H:%M")
        time.append(slot)
        time_slot = time_slot + timedelta(minutes=30)

    context = {
        'week': days,
        'time': time,
        'meeting_slot_info': weekly_data
    }

    html = render_template('calendar_template.html', context)
    return html


def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False


def main():
    form = cgi.FieldStorage()
    lecturer_id = form.getfirst("lecturer_id")
    startDate = form.getfirst(
        "start_date", datetime.today().strftime("%Y-%m-%d"))
    is_student_booking = str_to_bool(form.getfirst("student_booking", "True"))

    html = create_index_html(lecturer_id, startDate, is_student_booking)
    print("Content-type: text/html")
    print("\n")
    print(html)

########################################

if __name__ == "__main__":
    main()
