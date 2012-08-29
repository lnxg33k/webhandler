from os import path, getcwd
from subprocess import Popen, PIPE
from random import choice

from core.libs.thirdparty.termcolor import colored


class Banner(object):
    colors = ['red', 'yellow', 'green']
    banner = colored(choice([
"""
\t\t__          __  _     _    _                 _ _
\t\t\ \        / / | |   | |  | |               | | |
\t\t \ \  /\  / /__| |__ | |__| | __ _ _ __   __| | | ___ _ __
\t\t  \ \/  \/ / _ \ '_ \|  __  |/ _` | '_ \ / _` | |/ _ \ '__|
\t\t   \  /\  /  __/ |_) | |  | | (_| | | | | (_| | |  __/ |
\t\t    \/  \/ \___|_.__/|_|  |_|\__,_|_| |_|\__,_|_|\___|_|
\t\t-----------------------------------------------------------""",
"""
\t\t.-. . .-..----..----. .-. .-.  .--.  .-. .-..----. .-.   .----..----.
\t\t| |/ \| || {_  | {}  }| {_} | / {} \ |  `| || {}  \| |   | {_  | {}  }
\t\t|  .'.  || {__ | {}  }| { } |/  /\  \| |\  ||     /| `--.| {__ | .-. \\
\t\t`-'   `-'`----'`----' `-' `-'`-'  `-'`-' `-'`----' `----'`----'`-' `-'
\t\t----------------------------------------------------------------------""",
"""
\t\td  d  b d sss   d ss.  d    d d s.   d s  b d ss    d      d sss   d ss.
\t\tS  S  S S       S    b S    S S  ~O  S  S S S   ~o  S      S       S    b
\t\tS  S  S S       S    P S    S S   `b S   SS S     b S      S       S    P
\t\tS  S  S S sSSs  S sSS' S sSSS S sSSO S    S S     S S      S sSSs  S sS'
\t\tS  S  S S       S    b S    S S    O S    S S     P S      S       S   S
\t\t S  S S S       S    P S    S S    O S    S S    S  S      S       S    S
\t\t  "ss"S P sSSss P `SS  P    P P    P P    P P ss"   P sSSs P sSSss P    P
\t\t-------------------------------------------------------------------------""",
]), choice(colors))
    if not path.exists(path.join(getcwd(), ".git")):
        banner += colored('\n\t\t  [!] "non-git". Keep up-to-date by running \'--update\'', 'red')
    else:
        f = Popen('git rev-parse --short HEAD', shell=True, stdout=PIPE, stderr=PIPE)
        current_commit = f.communicate()[0]
        banner += colored('\n{0}Version: {1}'.format('\t' * 7, current_commit), 'grey', attrs=['bold'])

banner = Banner().banner
