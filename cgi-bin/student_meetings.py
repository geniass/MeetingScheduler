#!/usr/bin/env python3

import os
from jinja2 import Environment, FileSystemLoader

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, '../templates')),
    trim_blocks=False)


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def create_index_html():
    fname = "output.html"
    urls = ["Dr. Levitt", "Prof. Hazelhurst",
            "Dr. Nyandoro", "Dr. Shuma-Iwisi"]
    context = {
        'urls': urls
    }
    
    html = render_template('student_meetings.html', context)
    return html

def main():
    html = create_index_html()
    print('content-type: text/html \n')
    print(html)

if __name__ == "__main__":
    main()
