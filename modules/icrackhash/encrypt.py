from collections import OrderedDict

from hashlib import md5
from hashlib import sha256
from hashlib import sha224
from hashlib import sha1


class Encrypt(object):
    """
    >>> from encrypt import encrypt
    >>> for algo in encrypt.algos:
    ...     print algo, encrypt.algos[algo]('admin')
    """
    def __init__(self):
        self.algos = OrderedDict([
                      ('md5', self.md5),
                      ('sha1', self.sha1),
                      ('sha256', self.sha256),
                      ('sha224', self.sha224),
                      ('mysql5', self.mysql5),
                      ('mysql3', self.mysql3),
                      ])

    def md5(self, plain):
        return md5(plain).hexdigest().lower()

    def sha256(self, plain):
        return sha256(plain).hexdigest().lower()

    def sha1(self, plain):
        return sha1(plain).hexdigest().lower()

    def sha224(self, plain):
        return sha224(plain).hexdigest().lower()

    def mysql5(self, plain):
        return "*"+sha1(sha1(plain).digest()).hexdigest().lower()

    def mysql3(self, plain):
      "http://djangosnippets.org/snippets/1508/"
      nr = 1345345333
      add = 7
      nr2 = 0x12345671

      for c in (ord(x) for x in plain if x not in (' ', '\t')):
          nr^= (((nr & 63)+add)*c)+ (nr << 8) & 0xFFFFFFFF
          nr2= (nr2 + ((nr2 << 8) ^ nr)) & 0xFFFFFFFF
          add= (add + c) & 0xFFFFFFFF

      return "%08x%08x" % (nr & 0x7FFFFFFF,nr2 & 0x7FFFFFFF)

encrypt = Encrypt()
