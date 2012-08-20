import socket
import sys
import time

from core.libs.menu import getargs
from core.libs.thirdparty.termcolor import colored, cprint


class Listener(object):
    def __init__(self, port=None):
            self.port = getargs.listen

    def wait_connection(self):
        try:
            print colored('\n[i] Waiting on port: ', 'green') + colored(self.port, 'yellow')
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', self.port))
            server.listen(1)
            try:
                self.socket, self.address = server.accept()
                self.socket.setblocking(0)
                targetIP, targetPort = self.address
                cprint('[+] Received connection from: {0}'.format(targetIP), 'magenta')
                self.connected()
            except KeyboardInterrupt:
                cprint('\n[!] Lost connection. Exiting...', 'red')
        except socket.error:
            cprint('\n[!] Wasn\'t able to open a port. Make sure to run WebHanlder with a user which can (e.g. superuser)', 'red')
            exit(3)

    def connected(self):
        while True:
            try:
                buffer = self.socket.recv(1024)
                if buffer == '':
                    cprint('\n[!] Lost connection. Exiting...', 'red')
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
                    cprint('\n[!] Error in sending data', 'red')
                time.sleep(0.1)
            except KeyboardInterrupt:
                print ""
                pass

listen = Listener()
