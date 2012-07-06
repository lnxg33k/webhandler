from request_handler import make_request


class LinuxVersion(object):
    def __init__(self):
        self.url = make_request.url

    def get_doc_root(self):
        make_request.cmd = "echo \"<?php echo \$_SERVER['DOCUMENT_ROOT']; ?>\" > ~doc_root.php; [ -r ~doc_root.php ] && echo exists || echo not_exist"
        # make a request to create a php file thx @0xAli
        if make_request.get_page_source()[0] == 'exists':
            make_request.url = make_request.url.replace(make_request.url.split('/')[-1], '~doc_root.php')
            make_request.cmd = ''
            doc_root = make_request.get_page_source()[0]
            make_request.url = self.url
            make_request.cmd = "rm ~doc_root.php"
            make_request.get_page_source()
        else:
            correct_command = ['lsb_release -d', 'cat /etc/*-release']
            for command in correct_command:
                make_request.cmd = command
                distrib_description = make_request.get_page_source()[0].lower()
                if distrib_description:
                    if 'ubuntu' in distrib_description:
                        make_request.cmd = "grep -i \"DocumentRoot\" /etc/apache2/sites-available/default| awk '{print $2}'"
                        doc_root = make_request.get_page_source()[0]
                    elif 'centos' in distrib_description or 'fedora' in distrib_description or 'red hat' in distrib_description:
                        make_request.cmd = "grep -i 'DocumentRoot' /etc/httpd/conf/httpd.conf"
                        doc_root = make_request.get_page_source()[0]
                    else:
                        doc_root = None
                    break
                else:
                    pass

        return doc_root

linux = LinuxVersion()
