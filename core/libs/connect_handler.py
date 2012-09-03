import socket
import sys
import time

from core.libs.menu import getargs
from core.libs.banner import banner
from core.libs.thirdparty.termcolor import colored, cprint


class Connecter(object):
    def __init__(self, ip=None, port=None):
            if getargs.connect:     # Dirty hack!
                self.ip = getargs.connect.split(':')[0]
                self.port = int(getargs.connect.split(':')[1])

    def create_connection(self):
        try:
            print banner
            print colored('\n[i] Connecting to: ', 'green') + colored(str(self.ip), 'yellow') + colored(':', 'green') + colored(str(self.port), 'yellow')
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
            self.socket.setblocking(0)
            #self.socket.shutdown(socket.SHUT_WR)

        except socket.error:
            cprint('\n[!] Wasn\'t able to connect to: {0}, on port: {1}.'.format(self.ip, self.port), 'red')
            exit(3)
            
connect = Connecter()
