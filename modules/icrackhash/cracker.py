from smasher import hashType
from dbs import oneWay

from core.libs.thirdparty.termcolor import cprint, colored


def singleCrack(hash):
    if hashType(hash) in oneWay.algos:
        for db in oneWay.dbs:
            try:
                if oneWay.dbs[db](hash, hashType(hash)):
                    output = (oneWay.dbs[db](hash, hashType(hash)), hashType(hash), db)
                    return "\nhash: {0} \t plain: {1}  type: {2}  database: {3}".format(
                        colored(hash, 'white'),
                        colored(output[0], 'green'),
                        colored(output[1], 'white'),
                        colored(output[2], 'white')
                        )
                    break
                else:
                    return colored("{0} \t Not Found".format(hash), 'red')
            except:
                pass
    else:
        msg = colored("\n{0}: \t Not Detected.\n".format(hash), 'red')
        msg += colored('[+] Supported hashes [md5, sha1, sha224, sha256, mysql3, mysql4]', 'red')
        return msg


def help():
    cprint("\n[+] Usage: @crack <hash>", 'blue')
    cprint('[!] Example. @crack 21232f297a57a5a743894a0e4a801fc3', 'white')