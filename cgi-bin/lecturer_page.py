#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import os
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


def create_index_html(lecturer_id):
    context = {
        'lecturer_id': lecturer_id
    }

    html = render_template('lecturer_page.html', context)
    return html


def main():
    form = cgi.FieldStorage()
    lecturer_id = form.getfirst("lecturer_id")

    html = create_index_html(lecturer_id)
    print('Content-type: text/html\n')
    print(html)

if __name__ == "__main__":
    main()
