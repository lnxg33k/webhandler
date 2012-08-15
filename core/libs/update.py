from os import path, getcwd
from subprocess import Popen, PIPE

from core.libs.termcolor import cprint


def update():
    if not path.exists(path.join(getcwd(), ".git")):
        errmsg = '\n[!]".git" directory doesn\'t exist here.'
        errmsg += '\n[!] Clone webhandler (e.g. mv -f $(pwd){,_old} && git clone https://github.com/lnxg33k/webhandler.git $(pwd))'
        cprint(errmsg, 'red')
    else:
        f = Popen('git rev-parse --short HEAD', shell=True, stdout=PIPE, stderr=PIPE)
        current_commit = f.communicate()[0]
        msg = '\n[+] WebHandler current commit: {0}'.format(current_commit)
        msg += '[+] Update in progress, please wait...'
        cprint(msg, 'green')
        f = Popen('git pull; git rev-parse --short HEAD', shell=True, stdout=PIPE, stderr=PIPE)
        out, err = f.communicate()
        if out and not err:
            msg = '[+] Updated successfully to: {0}\n'.format(out.split()[-1])
            msg += '\n[i] Make sure to re-run WebHandler to use the updated version'
            cprint(msg, 'green')
        else:
            errmsg = '\n[!] \'git\' is required to update webhandler from CLI'
            errmsg += '\n[!] To install it (e.g. sudo apt-get install git OR sudo yum install git)'
            cprint(errmsg, 'red')
