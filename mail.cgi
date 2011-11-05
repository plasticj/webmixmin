#!/usr/bin/env python

import cgi
import cgitb
cgitb.enable()

MAIN_FORM="mail.html"

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

form = cgi.FieldStorage()
if "mailtext" in form and "recipient" in form:
    print "Submitted: "
    txt = form.getvalue("mailtext")
    print txt
    print "Recipient: "
    to = form.getvalue("recipient")
    print to
else:
    try:
        f = open(MAIN_FORM, "rb")
        main_content = f.readlines()
    except:
        cgi.sys.exit(1)

    print "".join(main_content)
