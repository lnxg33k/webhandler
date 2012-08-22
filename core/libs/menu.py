from core.libs.thirdparty import argparse


class GetArgs(object):
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
    general.add_argument('-nc', '--no-color', dest='color', help="\t\tDesable a colorful output.", action="store_true")

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
    color = options.color

getargs = GetArgs()
