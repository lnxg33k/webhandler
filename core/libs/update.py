from os import path, getcwd
from platform import platform as OS
from subprocess import Popen, PIPE

from core.libs.thirdparty.termcolor import cprint


def update():          
    if not path.exists(path.join(getcwd(), ".git")):
        errmsg = '\n[!] ".git" directory doesn\'t exist here.'
        cprint(errmsg, 'red')
        
        if Popen("git --version", shell=True, stdout=PIPE, stderr=PIPE).wait() != 0:
            errmsg = '\n[!] Didn\'t detect git. Therefore unable to update.'
            errmsg += '[!] Update: Aborted'
            cprint(errmsg, 'red')
            return
            
        msg = '\n[i] Detected git, cloning WebHandler'
        if 'windows' in OS().lower():
            command = "xcopy \"%CD%\" \"%CD%_old\" /E /C /I /G /H /R /Y && set rmdir=\"%CD%\" && cd %HOME% && rmdir %rmdir% /s /q & git clone https://github.com/lnxg33k/webhandler.git \"%CD%\""            
        else:
            command = "mv -f $(pwd){,_old} && git clone https://github.com/lnxg33k/webhandler.git \"$(pwd)\""
        msg = '\n[i] Executing: %s' % (command)
        cprint(msg, 'green')
        
        f = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        
        msg = '[+] Successfully upgrade to the latest git version'
        msg += '\n[i] Make sure to re-run WebHandler to use the updated version'
        cprint(msg, 'green')
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
            errmsg = '\n[!] \'git\' is required to update WebHandler from CLI'
            errmsg += '\n[!] e.g. sudo apt-get install git OR sudo yum install git. Else visit http://git-scm.com/'
            cprint(errmsg, 'red')
