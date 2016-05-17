#!/usr/bin/env python3

import os
from datetime import datetime, timedelta
from jinja2 import Environment, FileSystemLoader
#import cgi
#import cgitb
#cgitb.enable()

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
	autoescape=False,
	loader=FileSystemLoader(os.path.join(PATH, '../templates')),
	trim_blocks=False)


def render_template(template_filename, context):
	return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

def create_html(given_url):
	url = given_url
	context = {
		'url': url
	}
	html = render_template('monthly_calendar_template.html', context)
	return html

def main():
	#form = cgi.FieldStorage()
	#given_url = form.getfirst("startDate")

	given_url = '/'
	html = create_html(given_url)
	print("Content-type: text/html")
	print("\n")
	print(html)

########################################

if __name__ == "__main__":
	main()