from core.libs.request_handler import make_request
from core.libs.menu import Colors


class Enumerate(object):
    def health(self):
        cmd = 'input=`uptime` && if [[ \'$input\' == *day* ]] ; then echo $input | awk \'{print $3 ":" $5}\' | tr -d "," | awk -F ":" \'{print $1 " days, " $2 " hours and " $3 " minutes"}\'; else echo $input | awk \'{print $3}\' | tr -d "," | awk -F ":" \'{print $1 " hours and " $2 " minutes"}\'; fi;'
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
        #cmd += "awk '{split($4,a,\"/\"); printf a[1] \" (\"; printf a[2]\")\"}' /proc/loadavg;"

        health = make_request.get_page_source(cmd)

        print '\n{0}[+] Uptime: {1} {2}'.format(Colors.GREEN, health[0], Colors.END)
        print '{0}[+] Idletime: {1} {2}'.format(Colors.GREEN, health[0], Colors.END)
        print '{0}[+] Users Logged in: {1} {2}'.format(Colors.GREEN, health[1], Colors.END)
        print '{0}[+] Total Users: {1} {2}'.format(Colors.GREEN, health[2], Colors.END)
        print '{0}[+] Total Groups: {1} {2}'.format(Colors.GREEN, health[3], Colors.END)
        print '{0}[+] CPU Load (1, 5, 15 mins): {1} {2}'.format(Colors.GREEN, health[4], Colors.END)
        print '{0}[+] Memory Load (Used %): {1} {2}'.format(Colors.GREEN, health[5], Colors.END)
        print '{0}[+] Established TCP Connections: {1} {2}'.format(Colors.GREEN, health[6], Colors.END)
        print '{0}[+] Listening TCP Services: {1} {2}'.format(Colors.GREEN, health[7], Colors.END)
        print '{0}[+] User Processors: {1} {2}'.format(Colors.GREEN, health[8], Colors.END)
        print '{0}[+] Total Processor: {1} {2}'.format(Colors.GREEN, health[9], Colors.END)

enumerate = Enumerate()
