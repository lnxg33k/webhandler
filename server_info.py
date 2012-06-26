from urllib2 import urlopen, URLError, HTTPError
from request_info import RequestType
from menu import Colors, get_banner


class ServerInfo(RequestType):
    def get_information(self):
        try:
            self.source = source = map(str.strip, self.get_page_source().readlines())
            print  get_banner
        except HTTPError:
            print '\n[!] Invalid URL.'
            exit(1)
        try:
            local_ip = (urlopen('http://ifconfig.me/ip').read()).strip()
        except URLError:
            local_ip = 'Unknown'
        available_commands = ['exit', 'clear', 'history', 'info', 'banner', 'writable', 'spread']
        self.info = \
        '''
        {dashed}
        {red}User{end}     :  {green}{current_user}{end}
        {red}ID{end}       :  {green}{current_id}{end}
        {red}Kernel{end}   :  {green}{kernel_info}{end}
        {red}CWD{end}      :  {green}{cwd}{end}
        {red}Host IPs{end} :  {green}{host_ip}{end}
        {red}Local IP{end} :  {green}{local_ip}{end}
        {dashed}

        {hot}[+] Available commands: {available_commands}.{end}
        {hot}[+] Inserting{end} {red}!{end} {hot}at the begining of the command will execute it on your box.{end}
        '''.format(dashed='-' * int(len(source[2]) + 12),
                red=Colors.RED, green=Colors.GREEN, end=Colors.END, hot=Colors.HOT,
                current_user=source[0],
                current_id=source[1],
                kernel_info=source[2],
                cwd=source[3],
                host_ip=', '.join(source[4:]),
                local_ip=local_ip,
                available_commands=available_commands,)
        print self.info

serverinfo = ServerInfo()
