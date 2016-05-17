#!/usr/bin/env python3

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


def create_index_html(startDate):
    urls = ['List of Meetings', 'Bookings Management Page']
    meeting_details = dict(date='2016-05-14', user_id='1',
                           meeting_type='Cool Kid', year='4')
    days = requested_date(startDate)

    # Dummy data for the data from the database
    meeting_data = [dict(status='Book', link='www.google.com'), dict(status='Book', link='www.google.com'), dict(status='Book', link='www.google.com'), dict(status='Book', link='www.google.com'),
                    dict(status='Book', link='www.google.com'), dict(status='Edit', link='www.google.com'), dict(
                        status='Book', link=''), dict(status='Book', link='www.google.com'),
                    dict(status='Edit', link='www.google.com'), dict(status='Edit', link='www.google.com'), dict(
                        status='Edit', link='www.google.com'), dict(status='Busy', link=''),
                    dict(status='Busy', link=''), dict(status='Book', link='www.google.com'), dict(
                        status='Edit', link='www.google.com'), dict(status='Busy', link=''),
                    dict(status='Edit', link='www.google.com'), dict(status='Busy', link='')]

    weekly_data = dict()
    for j in range(7):
        label = days[j]
        weekly_data[label] = meeting_data

    time_slot = datetime.strptime("08:00", "%H:%M")
    time = []
    for k in range(18):
        slot = time_slot.strftime("%H:%M")
        time.append(slot)
        time_slot = time_slot + timedelta(minutes=30)

    context = {
        'urls': urls,
        'detail': meeting_details,
        'week': days,
        'time': time,
        'meeting_slot_info': weekly_data
    }
    #
    html = render_template('calendar_template.html', context)
    return html


def main():
    form = cgi.FieldStorage()
    startDate = form.getfirst("startDate")

    html = create_index_html(startDate)
    print("Content-type: text/html")
    print("\n")
    print(html)

########################################

if __name__ == "__main__":
    main()
