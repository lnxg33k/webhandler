#!/usr/bin/env python
# Written by Ahmed Shawky @lnxg33k

# importing modules
import sys
import urllib
import urllib2
import optparse

# help message when no-args supplied
if len(sys.argv) <= 1:
    print '''
    icode is a a simple script to upload your codes via CL
    to: http://code.isecur1ty.org  'thanks: aalgha' for it
    written be: Ahmed Shawky @lnxg33k ahmed@isecur1ty.org

    run -h for more options'''
    sys.exit(1)

# epilog message as an example
ex = '''
Examples:
./icode.py --email ahmed@isecur1ty.org --password ******* --file test.rb --type ruby
'''
# fixing epilog \n issue by subclassing the OptionParser
optparse.OptionParser.format_epilog = lambda self, formatter: self.epilog

parser = optparse.OptionParser(epilog=ex, add_help_option=False)
parser.add_option("-h", "--help", help="\t\tShow this help message and exit", action="help")
parser.add_option("--email", dest="mail", help="\t\tYour registered email address")
parser.add_option("--password", dest="pwd", help="\t\tThe passwrod for that email")
parser.add_option("--file",  dest="fname", help="\t\tThe file you want to upload")
parser.add_option("--type", dest="lang", help="\t\tThe language of the file")
parser.add_option("-t", "--types", dest="types", help="\t\tList available types", action="store_true")
(opts, args) = parser.parse_args()

mail = opts.mail
pwd  = opts.pwd
fname = opts.fname
lang = opts.lang

if opts.types:
    print '''
        [-] Available types:
        ---------------------
        1- text               11-javascript
        2- bash               12-css
        3- diff               13-c
        4- powershell         14-csharp
        5- ruby               15-vb
        6- python             16-delphi
        7- perl               17-java
        8- php                18-javafx
        9- sql                19-scala
        10-html               20-groovy'''

# solving dependencies issues
if not mail:
    print '\n[-] Email address is required\t--email'
if mail and not pwd:
    print '\n[-] Password is required\t--password'
if mail and not fname:
    print '\n[-] I need a file to upload\t--file'


if mail and pwd and fname:
    s = ''
    try:
        f = open(fname, 'rU')
        for line in f:
            s += line
        f.close()
    except IOError:
        print '\n[*] Erorr: %s doesn\'t exsit' % fname
        sys.exit(1)

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    urllib2.install_opener(opener)
    logs = urllib.urlencode({'email':mail, 'password':pwd})
    f = opener.open('http://code.isecur1ty.org/', logs)
    source = f.read()
    if 'error' in source:
        print '\n[-] Error: check your email and password'
        sys.exit(1)
    else: pass
    f.close()

    params = urllib.urlencode({'code':s, 'language':lang, 'direction':'ltr'})
    f = opener.open('http://code.isecur1ty.org/code', params)
    print '\n[-] Code uploaded successfully: %s' % f.geturl()
    f.close()
