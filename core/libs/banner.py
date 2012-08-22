from os import path, getcwd
from subprocess import Popen, PIPE

from core.libs.thirdparty.termcolor import colored


class Banner(object):
    banner = colored("""
\t\t__          __  _     _    _                 _ _
\t\t\ \        / / | |   | |  | |               | | |
\t\t \ \  /\  / /__| |__ | |__| | __ _ _ __   __| | | ___ _ __
\t\t  \ \/  \/ / _ \ '_ \|  __  |/ _` | '_ \ / _` | |/ _ \ '__|
\t\t   \  /\  /  __/ |_) | |  | | (_| | | | | (_| | |  __/ |
\t\t    \/  \/ \___|_.__/|_|  |_|\__,_|_| |_|\__,_|_|\___|_|
\t\t-----------------------------------------------------------""", 'yellow')

    if not path.exists(path.join(getcwd(), ".git")):
        banner += colored('\n\t\t  [!] "non-git". Keep up-to-date by running \'--update\'', 'red')
    else:
        f = Popen('git rev-parse --short HEAD', shell=True, stdout=PIPE, stderr=PIPE)
        current_commit = f.communicate()[0]
        banner += colored('\n{0}Version: {1}'.format('\t' * 7, current_commit), 'green')

banner = Banner().banner
