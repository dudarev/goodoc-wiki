#!/usr/bin/python
import os
import sys
import urllib2

from settings import *

def _get_html(url):
    "for url gets its html"
    response = urllib2.urlopen(url)
    html = response.read()
    return html

def _get_pages_data():
    """parse pages spreadsheet
    return list of pages of property:value dicts
    """
    
    raw_pages_file = os.path.join(RAW_PAGES_DIR, 'pages.html')
    pages = [] # list of property:value dicts
    from bs4 import BeautifulSoup as bs

    page = open(raw_pages_file, 'r').read()
    soup = bs(page)
    rows = soup.find_all('tr')

    # properties are stored in row 2 (link to page, date, changed, short link etc.)
    properties_row = 2
    properties = [p.text for p in rows[properties_row].find_all('td')]

    # TODO: print if verbose
    # print properties

    import re
    reg_doc = r'd/(.+)/edit'

    for row_data in rows[properties_row + 1:]:
        data = [d.text for d in row_data.find_all('td')]
        page = {}
        for p,d in zip(properties, data):
            # property name should be larger than
            if len(p) > 1:
                page[p] = d
        page['doc_id'] = re.findall(reg_doc, page['Link'])[0]

        pages.append(page)
    
    return pages

def _youtube_link_to_embed(html):
    """parse html
    find all youtube links in the format
    <a href="...">http://www.youtube.com/watch?v=4s4jluxdP4c&list=UUhcJt_ugtjjjr0RxOKhC61w&index=1&feature=plcp</a>
    and replace the whole tag with embeded code in format
    <iframe width="560" height="315" src="http://www.youtube.com/embed/4s4jluxdP4c" frameborder="0" allowfullscreen></iframe>
    """

# TODO: for future consideration - remove attributes
# https://gist.github.com/673417

def get():
    "downloads spreadsheet with list of pages and each HTML for each page"

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-n", "--no-pages", action="store_true", dest="no pages")
    (opts, args) = parser.parse_args(sys.argv[2:])

    raw_pages_file = os.path.join(RAW_PAGES_DIR, 'pages.html')

    if not getattr(opts,"no pages"):
        # download pages spreadsheet if -n option is NOT specified
        print "downloading link pages spreadsheet..."

        html = _get_html(PAGES_LINK)
        
        if not os.path.exists(RAW_PAGES_DIR):
            print "Creating directory for pages."
            os.makedirs(RAW_PAGES_DIR)
        
        f = open(raw_pages_file, 'w')
        f.write(html)
        f.close()
    else:
        print "pages spreadsheet is NOT downloaded"

    pages = _get_pages_data()

    # TODO: print if verbose
    # for p in pages:
    #    print p['Title']

    # TODO
    # Download pages
    # https://docs.google.com/document/d/1s4ke5WEmThv1y51hIAAbJhcq8At8eP7qCDv8rIi6258/edit?disco=AAAAAEfFcUA
    # https://docs.google.com/document/pub?id=1s4ke5WEmThv1y51hIAAbJhcq8At8eP7qCDv8rIi6258

    for p in pages:
        doc_id = p['doc_id']
        if doc_id:
            print "downloading doc_id %s" % doc_id

            html = _get_html('https://docs.google.com/document/pub?id=%s' % doc_id)
            raw_doc_file = os.path.join(RAW_PAGES_DIR, '%s.html' % doc_id)
            f = open(raw_doc_file, 'w')
            f.write(html)
            f.close()

def make():
    "create static pages based on templates"

    if not os.path.exists(SITE_DIR):
        print "Creating directory for site."
        os.makedirs(SITE_DIR)

    pages = _get_pages_data()

    from bs4 import BeautifulSoup as bs

    from jinja2 import Template
    template = Template(open(os.path.join(TEMPLATES_DIR, 'page.html'), 'r').read().decode('utf8'))

    for p in pages:
        # TODO: refactor this to _get_pages_data
        raw_doc_file = os.path.join(RAW_PAGES_DIR, '%s.html' % p['doc_id'])
        html = open(raw_doc_file, 'r').read()
        soup = bs(html)
        contents = soup.find("div", {"id": "contents"})
        page_file = os.path.join(SITE_DIR, '%s.html' % p['Short Link'])
        f = open(page_file, 'w')
        f.write(template.render(contents=contents, NAV_PAGES=NAV_PAGES, page=p).encode('utf8'))
        f.close()

    # create Pages page
    template = Template(open(os.path.join(TEMPLATES_DIR, 'all_pages.html'), 'r').read().decode('utf8'))
    page_file = os.path.join(SITE_DIR, 'Pages.html')
    f = open(page_file, 'w')
    f.write(template.render(pages=pages, NAV_PAGES=NAV_PAGES).encode('utf8'))
    f.close()

    from shutil import copy
    copy(
            os.path.join(SITE_DIR, 'Home.html'),
            os.path.join(SITE_DIR, 'index.html')
        )

def help():
    "prints help"
    print ""
    print "usage: python goodoc.py COMMAND [ARGS]"
    print ""
    print "commands:"
    print ""
    print "  get    downloads spreadsheet with list of pages and each HTML for each page"
    print "     -n  do not download pages spreadseet"
    print ""
    print "  make   creates static pages"
    print ""

def main():
    args = sys.argv
    command = None
    if len(args) > 1:
        command = args[1]

    if command == "get":
        get()
        return

    if command == "make":
        make()
        return

    if command in ["help", "-h", "--help", "-help"]:
        help()
        return

    print "use python goodoc.py help for help"


if __name__ == "__main__":
    main()
