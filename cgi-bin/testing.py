#!/usr/bin/env python3
 
import os
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
 
PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, '../html')),
    trim_blocks=False)
 
 
def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

def frange(x,y, jump):
    while x < y:
        yield x
        x += jump
 
def create_index_html():
    urls = ['List of Meetings', 'Bookings Management Page']
    meeting_details = dict(date='2016-05-14', user_id='1', meeting_type='Cool Kid', year='4')
    date = datetime.strptime(meeting_details['date'], "%Y-%m-%d")
    date2 = date.strftime("%Y-%m-%d")
    print(date)
    days = dict(empty='time/day', day1=date, day2=(date + timedelta(days=1) ), day3=(date + timedelta(days=2) ), day4=(date + timedelta(days=3) ), day5=(date + timedelta(days=4) ), day6=(date + timedelta(days=5) ), day7=(date + timedelta(days=6) ))
    the_stuff = ['True', 'True', 'False', 'True', 'The Good Stuff', 'More Good Stuff', 'False']
    time = frange(8.0, 17, 0.5)

    context = {
        'urls': urls,
        'detail': meeting_details,
        'week': days,
        'time': time,
        'stuff': the_stuff
    }
    #
    html = render_template('testing.html', context)
    return html
 
 
def main():
    html = create_index_html()
    print("Content-type: text/html")
    print("\n")
    print(html) 
 
########################################
 
if __name__ == "__main__":
    main()
