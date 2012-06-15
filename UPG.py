#!/usr/bin/env python
#
# -*- coding: utf-8 -*-
# Copyright 2011 lnxg33k <ahmed@isecur1ty.org>
#
# UPG.py > username and password generator in Python
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

# Importing modules
from sys import argv, exit
try:
    import argparse
except ImportError:
    print '\n[+] "argparse" module is requierd > By default in:- 2.7.x'
    print '[!] "debian based" run > apt-get install python-argparse'
    exit()
from time import time
from subprocess import Popen, PIPE
from random import random, shuffle, randrange, choice, randint

NAME    = 'Username and Password Generator [UPG]'
VERSION = '2.0'
AUTHOR  = 'Ahmed Shawky [http://lnxg33k.wordpress.com/ | @lnxg33k]'
BANNER  = r"""
	 .-.
	(0_0) 	+-----------------+
	.-|-> 	| UPG.py Ver #%s |
	_/ \_ 	+-----------------+
        """ % VERSION

def main():
    if len(argv) <= 1:
        parser.print_help()

parser = argparse.ArgumentParser(
        add_help=False,
        usage='%(prog)s [-h]',
        formatter_class=argparse.RawDescriptionHelpFormatter,                             # This will fix description and epilog format
        description='%s #v%s\nby: %s\n' % (NAME, VERSION, AUTHOR),
        epilog='''
        Examples:
        python %(prog)s -d adam john smith -t 1000 -o out.txt -u -r 1:9
        python %(prog)s -d Richard MacKenzie -v true -o out.txt -s -y 1990 2009
        python %(prog)s -d David Stallman -o out.txt -l -a "@ * #" -rc''')

positional = parser.add_argument_group('Positional arguments')
positional.add_argument('-d', dest='data',   help='Data that will randomly got mixed', nargs='+', metavar='')
positional.add_argument('-o', dest='output', help='Save generated data to a file| output', metavar='')

optional = parser.add_argument_group('Optional arguments')
optional.add_argument('-h', action='help',  help='Print this help message then exit')
optional.add_argument('-t', dest='thread',  help='Number of threads [Default: 500]', type=int, default=500, metavar='')
optional.add_argument('-s', dest='strip',   help='Strip white spaces from generated data', action='store_true')
optional.add_argument('-u', dest='upperit', help='Generate random data in upper case', action='store_true')
optional.add_argument('-rc', dest='randomc', help='Replace each character with random case value', action='store_true')
optional.add_argument('-r', dest='randomi', help='Append random integers to data [Example: 1:6]', metavar='')
optional.add_argument('-y', dest='years',   help='Append random years to data [Example: 1970 2012]', nargs=2, metavar='')
optional.add_argument('-a', dest='appendi', help='Append special chars to data [Example: $ # & * %%]', metavar='')
optional.add_argument('-l', dest='leetmod', help='Add data in the leet mode [Example: leet = 1337]', action='store_true')
optional.add_argument('-v', dest='verbos',  help='\'True\' to print current process [Default: False]', metavar='')
optional.add_argument('-c', dest='credits', help='Show me the version and some credits then exit', action='store_true')

args = parser.parse_args()
data = args.data
thread = args.thread
outfile = args.output
strip = args.strip
upperit = args.upperit
randomc = args.randomc
randomi = args.randomi
years = args.years
appendi = args.appendi
leetmod = args.leetmod
verbos = args.verbos
credits = args.credits
s = ''
leet_s = ''
chars = ['-','_','.']

if data and not outfile:                                                            #\
  print '\n[!] Error: Flag -o is required'                                          #\
  exit()                                                                            #-->  Check for dependencies
if outfile and not data:                                                            #/
  print '\n[!] Error: Flag -d is required'                                          #/
  exit()                                                                            #/
if data and outfile:
  def write(outfile):                                                               # Write func in case of stoppage or KeyboardInterrupt
    try:
      f = open(outfile, 'w+')
      f.write(s)
      f.flush()                                                                     # Flushing file to read it
      f.seek(0)                                                                     # The pointer will be at the 1st line
      lines = set(f.readlines())                                                    # 'set' func will sort generated data
      open(outfile, 'w').writelines(lines)
      stop = time()                                                                 # Stopping timer
      f.close()
      spent = stop-start                                                            # The spent time during the whole process
      l = len(open(outfile, 'r').readlines())                                       # Counting lines in the generated file
      f = Popen('du -bh %s' % outfile, shell=True, stdout=PIPE, stderr=PIPE)        # Examining the size of the output file
      (out, err) = f.communicate()
      si = out.split()[0]
      print '[-] *%s | %dL* sorted and saved into *%s* in *%.fS*' % (si, l, outfile, spent)
    except IOError, e:
      print '[!] Check this error: %s' % e

  print BANNER

  if randomi:                                                                       # Appending random integers as a list '-r'
    a = []
    randomi = randomi.split(':')
    if verbos == 'true' or verbos == 'True':
      print '[+] Appending random integers between "%d and %d"' % (int(randomi[0]), int(randomi[1]))
    try:
      for i in range(int(randomi[0]), int(randomi[1])+1):
        a += str(i)
    except ValueError:
      print '\n[!] Error: It should be something like this (-r 1:6)'
      exit()
    for i in range(thread):
      shuffle(a)
      chars.append("".join(a))

  if years:                                                                         # Appending random years into chars list '-y'
    if verbos == 'true' or verbos == 'True':
      print '[+] Appending random years between "%s and %s"' % (years[0], years[1])
    try:
      for i in range(thread):
        chars.append(str(randrange(int(years[0]), int(years[1]))))
    except ValueError:
      print '\n[!] Error: It should be something like this (-y 1990 2005)'
      exit()

  if appendi:                                                                       # Appending user input into chars list '-a'
    if verbos == 'true' or verbos == 'True':
      print '[+] Appending "%s" into the generated data' % appendi
    appendi = appendi.replace(' ', '')                                              # Stripping whitespaces from the input '@#*'
    for i in range(thread):
      for item in appendi:
        chars.append(item)

  if data:                                                                          # Shuffling Data in heuristic way
    start = time()                                                                  # Starting timer
    try:
      choise = ''                                                                   # Solving NameError issue
      if verbos == 'true' or verbos == 'True':
        print '[+] Shuffling data ....'
        choise += raw_input(' \-> [!] This operatin may increase the CPU usage! Be verbos? (y/n)[n]: ')
      else: print '[+] Upcoming operations may take some time ...'
      for i in range(thread):
        if choise.lower() == 'y':  print s
        else: pass
        try:
          shuffle(data, random)
          s += data[randrange(len(data))][0]+data[randrange(len(data))]+' '+data[randrange(len(data))]+'\n'
          s += data[randrange(len(data))][0]+data[randrange(len(data))]+'\n'
          s += data[randrange(len(data))]+' '+choice(chars)+'\n'
          s += choice(chars)+data[randrange(len(data))]+' '+data[randrange(len(data))][0]+data[randrange(len(data))]+'\n'
          s += data[randrange(len(data))]+' '+data[randrange(len(data))][0]+data[randrange(len(data))]+choice(chars)+'\n'
          s += data[randrange(len(data))][0]+choice(chars)+data[randrange(len(data))]+' '+data[randrange(len(data))]+'\n'
          s += data[randrange(len(data))]+' '+data[randrange(len(data))][0]+choice(chars)+data[randrange(len(data))]+'\n'
          s += data[randrange(len(data))]+' '+data[randrange(len(data))][0]+data[randrange(len(data))]+'\n'
          s += data[randrange(len(data))]+choice(chars)+data[randrange(len(data))]+'\n'
          s += data[randrange(len(data))][0]+data[randrange(len(data))]+choice(chars)+data[randrange(len(data))]+choice(chars)+'\n'
          s += data[randrange(len(data))]+' '+data[randrange(len(data))]+data[randrange(len(data))][0]+'\n'
          s += data[randrange(len(data))]+choice(chars)+data[randrange(len(data))]+' '+data[randrange(len(data))]+'\n'
          s += data[randrange(len(data))]+choice(chars)+data[randrange(len(data))]+' '+choice(chars)+'\n'
          s += data[randrange(len(data))]+' '+data[randrange(len(data))]+choice(chars)+data[randrange(len(data))][0]+'\n'
          s += data[randrange(len(data))]+choice(chars)+data[randrange(len(data))][0]+' '+data[randrange(len(data))]+'\n'
          s += data[randrange(len(data))][0]+data[randrange(len(data))][0]+' '+data[randrange(len(data))]+'\n'
          s += data[randrange(len(data))]+' '+data[randrange(len(data))][0]+data[randrange(len(data))][0]+'\n'
          s += data[randrange(len(data))]+data[randrange(len(data))][0]+' '+data[randrange(len(data))]+'\n'
        except TypeError: pass

      if upperit:                                                                   # Adding uppercase to generated data '-u'
        if verbos == 'true' or verbos == 'True':
          print '[+] Converting Data into Upper Case ...'
        s += s.upper()

      if strip:                                                                     # Stripping whitespaces from generated data '-s'
        if verbos == 'true' or verbos == 'True':
          print '[+] Stripping white spaces from data ...'
        s += s.replace(' ', '')

      if randomc:                                                                   # Replacing each character with random case value '-rc'
        if verbos == 'true' or verbos == 'True':
          print '[+] Replacing each character with it\'s random case value ...'
        def randomRange(start=0, stop=1000):                                        # Function for choosing a random number within the range
          return int(randint(start, stop))                                          # This function is from sqlmap 'adam john' >> 'AdAm JOHn'
        for i in xrange(len(s)):
          if randomRange(0, 1):
            s += s[i].upper()
          else:
            s += s[i].lower()

      if leetmod:                                                                   # Leet mode 'leet haxor' >> '1337 h4x0r' '-l'
        if verbos == 'true' or verbos == 'True':
          print '[+] 1337!n9 7h3 0u7pu7 b3f0r3 54v!n9 !7 ...'
          print ' \-> [!] This operation may take some time ...'
        leet_s = s                                                                  # Assign data before converting it
        charlist = {'a': '4',                                                       # Dict of chars to be converted
                    'e': '3',
                    'l': '1',
                    'o': '0',
                    's': '5',
                    't': '7',
                    'i': '!',
                    'z': '2',
                    'g': '9'}
        for i in leet_s.strip('\n'):
          if charlist.has_key(i):                                                   # CMP between chars in leet_s and keys in the DICT
            leet_s = leet_s.replace(i, charlist.get(i))
        s += leet_s

      if outfile:                                                                   # Save generated data into a file '-o'
        if verbos == 'true' or verbos == 'True':
          print '[+] Saving generated data into "%s"' % outfile
        write(outfile)

    except KeyboardInterrupt:
      print '\n[!] Terminated by user ....'
      s += leet_s
      write(outfile)

if credits:
  print '%s\n[+] %s #v%s\n[+] By: %s' % (BANNER, NAME, VERSION, AUTHOR)
  print """[+] Credits fly to:
 |_-> Rel1k, g0tmi1k, Eph, Connection, stamparm and LeXel
   -> Arabpwn: Saad, Menna, k4c0de, Obzy, Mohab and _nu11_"""

if __name__ == '__main__':
  main()
