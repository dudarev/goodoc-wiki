#!/usr/bin/python
import os
import sys
import urllib2

from settings import *

def get_html(url):
    "for url gets its html"
    response = urllib2.urlopen(PAGES_LINK)
    html = response.read()
    return html

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

        html = get_html(PAGES_LINK)
        print html
        
        if not os.path.exists(RAW_PAGES_DIR):
            print "Creating directory for pages."
            os.makedirs(RAW_PAGES_DIR)
        
        f = open(raw_pages_file, 'w')
        f.write(html)
        f.close()
    else:
        print "pages spreadsheet is NOT downloaded"

    # parse pages spreadsheet
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

    for row_data in rows[properties_row + 1:]:
        data = [d.text for d in row_data.find_all('td')]
        page = {}
        for p,d in zip(properties, data):
            # property name should be larger than
            if len(p) > 1:
                page[p] = d
        pages.append(page)

    # TODO: print if verbose
    # for p in pages:
    #    print p['Title']

    # TODO
    # Download pages
    # https://docs.google.com/document/d/1s4ke5WEmThv1y51hIAAbJhcq8At8eP7qCDv8rIi6258/edit?disco=AAAAAEfFcUA
    # https://docs.google.com/document/pub?id=1s4ke5WEmThv1y51hIAAbJhcq8At8eP7qCDv8rIi6258
    import re
    reg = r'd/(.+)/edit'
    for p in pages:
        print p["Link"]
        if p["Link"]:
            doc_id = re.findall(reg, p['Link'])[0]
            print doc_id

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

def main():
    args = sys.argv
    command = None
    if len(args) > 1:
        command = args[1]

    if command == "get":
        get()
        return

    if command in ["help", "-h", "--help", "-help"]:
        help()
        return

    print "use python goodoc.py help for help"


if __name__ == "__main__":
    main()
