import socket
import sys
import time

from core.libs.menu import getargs
from core.libs.banner import banner
from core.libs.thirdparty.termcolor import colored, cprint


class Listener(object):
    def __init__(self, port=None):
            self.port = getargs.listen

    def wait_connection(self):
        try:
            print banner
            print colored('\n[i] Waiting on port: ', 'green') + colored(str(self.port), 'yellow')
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', self.port))
            server.listen(1)
            try:
                self.socket, self.address = server.accept()
                self.socket.setblocking(0)
                targetIP, targetPort = self.address
                cprint('[+] Received connection from: {0}'.format(targetIP), 'magenta')
            except KeyboardInterrupt:
                cprint('\n[!] Lost connection. Exiting...', 'red')
        except socket.error:
            cprint('\n[!] Wasn\'t able to open a port. Make sure to run WebHandler with a user which can (e.g. superuser)', 'red')
            exit(3)

listen = Listener()
