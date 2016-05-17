#!/usr/bin/env python3
 
import os
from jinja2 import Environment, FileSystemLoader
 
PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, '../html')),
    trim_blocks=False)
 
 
def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

 
def create_index_html():
    urls = ['List of Meetings', 'Bookings Management Page']
    context = {
        'urls': urls
    }
    #
    html = render_template('lecturers_page.html', context)
    return html
 
 
def main():
    html = create_index_html()
    print("Content-type: text/html")
    print("\n")
    print(html) 
 
########################################
 
if __name__ == "__main__":
    main()

