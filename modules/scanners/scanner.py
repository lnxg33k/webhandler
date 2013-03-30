from core.libs.shell_handler import linux
from core.libs.file_handler import file_handler
from core.libs.request_handler import make_request
from core.libs.thirdparty.termcolor import cprint, colored


class Scanner(object):
    def help(self):
        msg = colored('\n[+] Usage: @scan <host> <range>\n', 'blue')
        msg += colored('Example. @scan 127.0.0.1 1-2000', 'white')
        print(msg)

    def scan_host(self, host, range):
        folder = linux.get_writble_dir()
        if folder:
            cprint('[+] Uploading scanner to the box ...', 'green')
            scanner = folder + '/webhandler_scanner.php'
            file_handler.upload_file('modules/scanners/port.php', scanner)
            cmd = 'cd {0}; php {1} {2} {3}'.format(folder, scanner, host, range)
            cprint('\n[+] Scanning the target ...', 'green')
            cprint('----------------------------')
            try:
                output = make_request.get_page_source(cmd)
                if output:
                    print ""
                    for line in output:
                        cprint(line, 'white')
                else:
                    cprint('\n[+] Didn\'t find any open ports match the range "{0}"'.format(range), 'red')

                file_handler.clean(scanner)
            except KeyboardInterrupt:
                file_handler.clean(scanner)

scanner = Scanner()
