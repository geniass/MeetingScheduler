#!/usr/bin/env python3
 
import os
from jinja2 import Environment, FileSystemLoader
 
PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, '../templates')),
    trim_blocks=False)
 
 
def render_template(template_filename):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render()

 
def create_html():
    html = render_template('lecturers_page.html')
    return html
 
 
def main():
    html = create_html()
    print("Content-type: text/html")
    print("\n")
    print(html) 
 
if __name__ == "__main__":
    main()

