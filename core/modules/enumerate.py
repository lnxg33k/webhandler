from core.libs.menu import Colors
from core.libs.request_handler import make_request
from core.modules.shell_handler import linux


class Enumerate(object):
    def list(self):
        print '\n[i] Usage: @enum [module]'
        print '[i] Modules:'
        print '[i] \thistory   \t\tList \'intressing\' (~/.*-history files)'
        print '[i] \tkeys      \t\tList private SSH & SSL keys/certs'
        print '[i] \tnetwork        \t\tGeneral networking infomation about the system'
        print '[i] \tos        \t\tGeneral operating system infomation'
        print '[i] \tsystem    \t\tGeneral infomation about the system'
        print '[i] \twritable\t\tList writable paths within the document\'s root directory'  
        
    def system(self):
        cmd = 'bash -c "input=\$(uptime); if [[ \$input == *day* ]]; then out=\$(echo \$input | awk \'{print \$3\\" days\\"}\'); if [[ \$input == *min* ]]; then out=\$(echo \\"\$out and \\" && echo \$input | awk \'{print \$5\\" minutes\\"}\'); else out=\$(echo \\"\$out, \\" && echo \$input | awk \'{print \$5}\' | tr -d \\",\\" | awk -F \\":\\" \'{print \$1\\" hours and \\"\$2\\" minutes\\"}\'); fi elif [[ \$input == *min* ]]; then out=\$(echo \$input | awk \'{print \$3\\" minutes\\"}\'); else out=\$(echo \$input | awk \'{print \$3}\' | tr -d \\",\\" | awk -F \\":\\" \'{print \$1\\" hours and \\"\$2\\" minutes\\"}\'); fi; echo \$out;" ;'
        cmd += "awk '{print ($1/(60*60*24))/($2/(60*60*24))*100 \"%\"}' /proc/uptime;"
        cmd += "w -h | wc -l;"
        cmd += "wc -l /etc/passwd | awk '{print $1}';"
        cmd += "wc -l /etc/group | awk '{print $1}';"
        cmd += "awk '{print $1 \" \" $2 \" \" $3}' /proc/loadavg;"
        cmd += "free -m | grep 'buffers/cache' | awk '{print $3*100/($3+$4)}';"
        cmd += "netstat -tn | grep ESTABLISHED | wc -l | awk '{print $1}';"
        cmd += "netstat -atn | grep LISTEN | wc -l | awk \"{print $1}\";"
        cmd += "awk '{split($4,a,\"/\"); print a[1];}' /proc/loadavg;"
        cmd += "awk '{split($4,a,\"/\"); print a[2];}' /proc/loadavg;"

        system = make_request.get_page_source(cmd)

        print '\n{0}[+] Uptime: {1}{2}'.format(Colors.GREEN, system[0], Colors.END)
        print '{0}[+] Idletime: {1}{2}'.format(Colors.GREEN, system[1], Colors.END)
        print '{0}[+] Users Logged in: {1}{2}'.format(Colors.GREEN, system[2], Colors.END)
        print '{0}[+] Total Users: {1}{2}'.format(Colors.GREEN, system[3], Colors.END)
        print '{0}[+] Total Groups: {1}{2}'.format(Colors.GREEN, system[4], Colors.END)
        print '{0}[+] CPU Load (1, 5, 15 mins): {1}{2}'.format(Colors.GREEN, system[5], Colors.END)
        print '{0}[+] Memory Load (Used %): {1}{2}'.format(Colors.GREEN, system[6], Colors.END)
        print '{0}[+] Established TCP Connections: {1}{2}'.format(Colors.GREEN, system[7], Colors.END)
        print '{0}[+] Listening TCP Services: {1}{2}'.format(Colors.GREEN, system[8], Colors.END)
        print '{0}[+] User Processors: {1}{2}'.format(Colors.GREEN, system[9], Colors.END)
        print '{0}[+] Total Processor: {1}{2}'.format(Colors.GREEN, system[10], Colors.END)

    def ip(self):
        cmd = "ip addr show | grep inet | awk '{printf \", \" $2}' | sed 's/^, *//' && echo;"
        cmd += "curl http://ifconfig.me/ip;"
        cmd += "cat /etc/resolv.conf | grep nameserver | awk '{printf \", \" $2}' | sed 's/^, *//' && echo;"
        cmd += "/sbin/route -n | awk '{print $2}' | grep -v 0.0.0.0 | grep -v IP | grep -v Gateway | head -n 1;"
        #grep -q "BOOTPROTO=dhcp" /etc/sysconfig/network-scripts/ifcfg-eth0 2>/dev/null
        #grep -q "inet dhcp" /etc/network/interfaces 2>/dev/null
        cmd += 'dhcp_ip=`grep dhcp-server /var/lib/dhcp*/dhclient.* 2>/dev/null | uniq | awk \'{print $4}\' | tr -d ";"`; if [ $dhcp_ip ] ; then echo "Yes ($dhcp_ip)"; else echo "No"; fi;'

        ip = make_request.get_page_source(cmd)

        print '\n{0}[+] Internal IP/subnet: {1}{2}'.format(Colors.GREEN, ip[0], Colors.END)
        print '{0}[+] External IP: {1}{2}'.format(Colors.GREEN, ip[1], Colors.END)
        print '{0}[+] DNS: {1}{2}'.format(Colors.GREEN, ip[2], Colors.END)
        print '{0}[+] Gateway: {1}{2}'.format(Colors.GREEN, ip[3], Colors.END)
        print '{0}[+] DHCP? : {1}{2}'.format(Colors.GREEN, ip[4], Colors.END)

    def os(self):
        cmd = "hostname;"
        cmd += "uname -a;"
        #cmd += "grep DISTRIB_DESCRIPTION /etc/*-release | head -n 1;"
        cmd += "cat /etc/*-release | head -n 1 | sed 's/DISTRIB_ID=//';"
        cmd += "date;"
        cmd += "zdump UTC | sed 's/UTC  //';"
        #cmd += "python -c 'import locale; print locale.getdefaultlocale()[0];';"
        cmd += "echo $LANG;"

        os = make_request.get_page_source(cmd)

        print '\n{0}[+] Hostname: {1}{2}'.format(Colors.GREEN, os[0], Colors.END)
        print '{0}[+] Kernel: {1}{2}'.format(Colors.GREEN, os[1], Colors.END)
        print '{0}[+] OS: {1}{2}'.format(Colors.GREEN, os[2], Colors.END)
        print '{0}[+] Local Time: {1}{2}'.format(Colors.GREEN, os[3], Colors.END)
        print '{0}[+] Timezone (UTC): {1}{2}'.format(Colors.GREEN, os[4], Colors.END)
        print '{0}[+] Language: {1}{2}'.format(Colors.GREEN, os[5], Colors.END)

    def keys(self):
        cmd = "find / -type f -print0 | xargs -0 -I '{}' bash -c 'openssl x509 -in {} -noout > /dev/null 2>&1; [[ $? == '0' ]] && echo \"{}\"'"
        self.ssl = make_request.get_page_source(cmd)
        if self.ssl:
            c = 1
            for path in self.ssl:
                print '{0:2d}- {1}'.format(c, path)
                c += 1
        else:
            print '\n{0}[!] Didn\'t find any SSL certs{1}'.format(Colors.RED, Colors.END)

        cmd = "find / -type f -print0 | xargs -0 -I '{}' bash -c 'openssl x509 -in {} -noout > /dev/null 2>&1; [[ $? == '0' ]] && echo \"{}\"'"
        self.sshpub = make_request.get_page_source(cmd)
        if self.sshpub:
            c = 1
            for path in self.sshpub:
                print '{0:2d}- {1}'.format(c, path)
                c += 1
        else:
            print '\n{0}[!] Didn\'t find any public SSH keys{1}'.format(Colors.RED, Colors.END)

        # Private keys
        #find / -type f -exec bash -c 'ssh-keygen -yf {} >/dev/null 2>&1' \; -exec bash -c 'echo {}' \;        #grep -r "SSH PRIVATE KEY FILE FORMAT" /{etc,home,root} 2> /dev/null | wc -l    # find / -name "*host_key*"

    # A method to get all writable directories within CWD
    def writable(self):
        cmd = "find {0} -depth -perm -0002 -type d".format(linux.get_doc_root())
        self.writable = make_request.get_page_source(cmd)
        if self.writable:
            c = 1
            for path in self.writable:
                print '{0}{1:2d}- {2}{3}'.format(Colors.GREEN, c, path, Colors.END)
                c += 1
        else:
            print '\n{0}[!] Didn\'t find any wriable directories{1}'.format(Colors.RED, Colors.END)

    def history(self):
        cmd = 'for i in $(cut -d: -f6 /etc/passwd | sort | uniq); do [ -f $i/.bash_history ] && echo "bash_history: $i"; [ -f $i/.nano_history ] && echo "nano_history: $i"; [ -f $i/.atftp_history ] && echo "atftp_history: $i"; [ -f $i/.mysql_history ] && echo "mysql_history: $i"; [ -f $i/.php_history ] && echo "php_history: $i";done'
        self.history = make_request.get_page_source(cmd)
        if self.history:
            c = 1
            for path in self.history:
                print '{0:2d}- {1}'.format(c, path)
                c += 1
        else:
            print '\n{0}[!] Didn\'t find any \'history\' files{1}'.format(Colors.RED, Colors.END)

enumerate = Enumerate()
