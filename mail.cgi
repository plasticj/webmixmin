#!/usr/bin/env python

import cgi
# debug
import cgitb
cgitb.enable()

import subprocess
import tempfile

MAIN_FORM="mail.html"

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

vardict = {'status' : '',
        'subj' : '',
        'recp' : '',
        'text' : '',
        }

form = cgi.FieldStorage()
if "mailtext" in form and "recipient" in form and "subject" in form:
    txt = form.getvalue("mailtext")
    to = form.getvalue("recipient")
    subj = form.getvalue("subject")

    vardict['text'] = txt
    vardict['recp'] = to
    vardict['subj'] = subj
    f = tempfile.NamedTemporaryFile()
    f.write(txt)
    f.file.flush()
    inputfile = f.name

    args = ['mixminion', 'send', 
            '--subject=%s' % subj,
            '-t', '%s' % to,]
#            '-i %s' % inputfile]
#    print " ".join(args)
    p0 = subprocess.Popen(args, stderr=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stdin=subprocess.PIPE)
    out, err = p0.communicate(txt)
    vardict['status'] = "output: %s stderr: %s" % (out, err)
    f.close()

try:
    f = open(MAIN_FORM, "rb")
    main_content = f.read()
except:
    cgi.sys.exit(1)

for k,v in vardict.items():
    main_content = main_content.replace("{$%s}" % k, v)
print "".join(main_content)
