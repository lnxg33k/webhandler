from os import path, getcwd
from platform import platform as OS
from subprocess import Popen, PIPE

from core.libs.thirdparty.termcolor import cprint

import os, sys


def update():        
    baseFolder = path.join(os.path.dirname(__file__),os.pardir , os.pardir) # ./core/libs/update.py
    if not path.exists(path.join(getcwd(), "webhandler.py")):
        errmsg = '[!] Unable to update WebHandler without being in the base folder.'
        errmsg += '\n[i] E.g. "cd {0}", and then try again.'.format(baseFolder)
        cprint(errmsg, 'red')
        sys.exit(1)
        
    if Popen("git --version", shell=True, stdout=PIPE, stderr=PIPE).wait() != 0:
        errmsg = '\n[!] Didn\'t detect git. Therefore unable to update.'
        errmsg += '\n[!] e.g. sudo apt-get install git OR sudo yum install git. Else visit http://git-scm.com/'
        errmsg += '[!] Update: Aborted'
        cprint(errmsg, 'red')
        return        
    
    if not path.exists(path.join(baseFolder, ".git")):
        errmsg = '\n[!] ".git" directory doesn\'t exist here.'
        cprint(errmsg, 'red')
                    
        msg = '\n[i] Detected git, cloning WebHandler'
        if 'windows' in OS().lower():
            command = "xcopy \"%CD%\" \"%CD%_old\" /E /C /I /G /H /R /Y && set rmdir=\"%CD%\" && cd %HOME% && rmdir %rmdir% /s /q & git clone https://github.com/lnxg33k/webhandler.git \"%CD%\""            
        else:
            command = "mv -f {0}/{,_old} && git clone https://github.com/lnxg33k/webhandler.git \"{0}/\"".format(baseFolder)
        msg = '\n[i] Executing: %s' % (command)
        cprint(msg, 'green')
        
        f = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        
        msg = '[+] Successfully upgrade to the latest git version'
        msg += '\n[i] Make sure to re-run WebHandler to use the updated version'
        cprint(msg, 'green')
    else:
        f = Popen('git rev-parse --short HEAD', shell=True, stdout=PIPE, stderr=PIPE) #cwd=baseFolder
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
            errmsg = '\n[!] Unable to update'
            errmsg += '\n[!] Make sure you have an internet connection'           
            cprint(errmsg, 'red')
