import os
from core.libs.request_handler import make_request
from core.libs.menu import Colors


class FileHandler(object):
    # A method for downloading files from the box
    def download_file(self, rfile_path, lfile_path):
        cmd = 'if [ -e {0} ]; then if [ -f {0} ]; then echo "file"; else echo "dir"; fi; fi'.format(rfile_path)
        file_type = make_request.get_page_source(cmd)[0]
        if file_type == 'file':
            cmd = 'cat {0}'.format(rfile_path)
            try:
                with open(lfile_path, 'w') as dest_file:
                    dest_file.write('\n'.join(make_request.get_page_source(cmd)))
                print '\n[+] Successfully downloaded "{0}" to "{1}"'.format(rfile_path, lfile_path)
            except IOError, e:
                print '\n{0}[!] {1}{2}'.format(Colors.RED, e, Colors.END)
        elif file_type == 'dir':
            cmd = 'find {0} | while read f;do echo "$f";done'.format(rfile_path)
            files = make_request.get_page_source(cmd)
            for file in files:
                cmd = 'if [ -e {0} ]; then if [ -f {0} ]; then echo "file"; else echo "dir"; fi; fi'.format(file)
                file_type = make_request.get_page_source(cmd)[0]
                if file_type == 'dir':
                    os.makedirs(os.path.join(lfile_path, file))
                elif file_type == 'file':
                    cmd = 'cat {0}'.format(file)
                    try:
                        with open(os.path.join(lfile_path, file), 'w') as dest_file:
                            dest_file.write('\n'.join(make_request.get_page_source(cmd)))
                    except IOError, e:
                        print '\n{0}[!] Error: {1}{2}'.format(Colors.RED, e, Colors.END)
                else:
                    print '{0}[!] Coudln\'t download the following file: {1}{2}'.format(Colors.RED, Colors.END, file)
            print '\n{0}[+] Files downloaded successfully to: {1}{2}'.format(Colors.GREEN, Colors.END, lfile_path)
        else:
            print '\n{0}[!]The file/directory doesn\'t exist or I don\'t have permission{1}'.format(Colors.RED, Colors.END)



    # A method for uploading files to the box
    def upload_file(self, lfile_path, rfile_path):
        with open(lfile_path) as local_file:
            data_to_upload = local_file.readlines()
        for line in data_to_upload:
            cmd = 'echo {0} >> {1}'.format(line.strip(), rfile_path)
            make_request.get_page_source(cmd)
        print '\n[+] Successfully uploaded {0} to {1}'.format(lfile_path, rfile_path)

file_handler = FileHandler()
