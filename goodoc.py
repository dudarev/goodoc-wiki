#!/usr/bin/python
import os
import sys

from settings import *


def get():
    "downloads spreadsheet with list of pages and each HTML for each page"

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-n", "--no-pages", action="store_true", dest="no pages")
    (opts, args) = parser.parse_args(sys.argv[2:])

    if not getattr(opts,"no pages"):
        # download pages spreadsheet if -n option is NOT specified
        print "downloading link pages spreadsheet..."

        import urllib2
        response = urllib2.urlopen(PAGES_LINK)
        html = response.read()

        if not os.path.exists(RAW_PAGES_DIR):
            print "Create directory for pages."
            os.makedirs(RAW_PAGES_DIR)
        
        f = open(os.path.join(RAW_PAGES_DIR, 'pages.html'), 'w')
        f.write(html)
    
    else:
        print "pages spreadsheet is NOT downloaded"

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
