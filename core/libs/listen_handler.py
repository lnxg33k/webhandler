import platform
import socket
import sys
import time

from core.libs.menu import getargs, Colors


class Listener(object):
    def __init__(self, port=None):
        if getargs.mode == "listen":
            self.port = int(getargs.listen)

    def wait_connection(self):
        os = platform.platform()
        if "windows" in os.lower():
            print '\n{0}[!] This feature isn\'t (yet) supported when used on a Windows operating system{1}'.format(Colors.RED, Colors.END)
            exit(2)

        print '\n{0}[i] Waiting on port: {1}{2}'.format(Colors.GREEN, self.port, Colors.END)
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', self.port))
            server.listen(1)
            self.socket, self.address = server.accept()
            self.socket.setblocking(0)
            targetIP, targetPort = self.address
            print '{0}[+] Received connection from: {1}{2}'.format(Colors.HOT, targetIP, Colors.END)
        except socket.error:
            print '\n{0}[!] Wasn\'t able to open a port. Make sure to run WebHanlder with a user which can (e.g. superuser){1}'.format(Colors.RED, Colors.END)
            exit(3)

    def connected(self):
        while True:
            try:
                buffer = self.socket.recv(1024)
                if buffer == '':
                    print '\n{0}[!] Lost connection. Exiting...{1}'.format(Colors.RED, Colors.END)
                    self.socket.close()
                    exit(1)
                while buffer != '':
                    sys.stdout.write(buffer)
                    sys.stdout.flush()
                    buffer = self.socket.recv(1024)
            except socket.error:
                pass

            try:
                cmd = raw_input("Command [>]: ")
                if(self.socket.sendall(cmd + "\n") != None):
                    print '\n{0}[!] Error in sending data{1}'.format(Colors.RED, Colors.END)
                time.sleep(0.1)
            except KeyboardInterrupt:
                print ""
                pass

listen = Listener()
