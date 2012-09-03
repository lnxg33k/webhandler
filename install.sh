#!/bin/sh

if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

chmod -R 700 "$(pwd)/webhandler.py"

ln -s "$(pwd)/webhandler.py" /bin/webhandler
ln -s "$(pwd)/webhandler.py" /bin/wh

./webhandler.py --update
