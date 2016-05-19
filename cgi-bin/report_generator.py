#!/usr/bin/env python3
from db import meeting

import os
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
import cgi
import cgitb
import sqlite3
cgitb.enable()

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, '../templates')),
    trim_blocks=False)


def render_template(template_filename, content):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(content)


def requested_date(start_date, end_date):
    startDate = datetime.strptime(start_date, "%Y-%m-%d")
    startDate = startDate.date()
    endDate = datetime.strptime(end_date, "%Y-%m-%d")
    endDate = endDate.date()
    dates = []
    current_date = startDate
    counter = 0
    while current_date != endDate:
        current_date = startDate + timedelta(days=counter)
        dates.append(current_date)
        counter = counter + 1
    return dates

def create_html(lecture_id, startDate, endDate):
    meeting_details = dict()
    dates = requested_date(startDate, endDate)
    for date in dates:
        detail = []
        ms = meeting.get_all_on(lecture_id, date)
        for m in ms:
            detail.append({'meeting_summary': m.subject, 'duration': m.duration})
        meeting_details[date] = detail
    content = {
    'meeting_details': meeting_details,
    'dates': dates
    }
    html = render_template('report_page.html', content)
    return html


def main():
    form = cgi.FieldStorage()
    startDate = form.getfirst("sdate")
    endDate = form.getfirst("edate")
    lecture_id = str(form.getfirst("lecturer_id"))

    html = create_html(lecture_id, startDate, endDate)
    print("Content-type: text/html")
    print("\n")
    print(html) 

if __name__ == "__main__":
    main()