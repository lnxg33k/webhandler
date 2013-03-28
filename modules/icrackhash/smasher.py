#!/usr/bin/python
# This script is a part of iCrackHash project
# Written by Ahmed Shawky @lnxg33k

from strop import lowercase as lcase
from strop import uppercase as ucase


def hashType(hash):
    # algos depend on iCrackHash's DB 'Rainbow Tables'
    if (hash.endswith(tuple('%s' % i for i in range(10))) \
    or hash.endswith(tuple(lcase[:6])) \
    or hash.endswith(tuple(ucase[:6]))):               # ^[A-Fa-f0-9]
        if len(hash) == 32:
            return 'md5'

        elif len(hash) == 41 \
        and hash.startswith('*'):
            return 'mysql5'

        elif len(hash) == 16:
            return 'mysql3'

        elif len(hash) == 40:
            return 'sha1'

        elif len(hash) == 64:
            return 'sha256'

        elif len(hash) == 56:
            return 'sha224'

        else:
            return None

    else:
        return None
