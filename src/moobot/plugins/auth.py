from ConfigParser import NoOptionError
from random import getrandbits
from struct import pack
from hashlib import sha256
from base64 import encodestring
from moobot.plugins import PassiveProvider

class AuthProvider(PassiveProvider):
    name = "auth"
    description = "Respond to authentication challenges"

    def run(self, target, *args):
        try:
            secret = '%08s' % (self.bot.config.get('auth', target)[:8],)
        except NoOptionError:
            # Don't have a secret for you, fail
            return None

        if len(args) < 1:
            c.privmsg(target, "huh?")
            return None

        # Server sends a unique challenge value sc to the client
        sc = args[0]

        # Client generates unique challenge value cc
        cc = pack('>Q', getrandbits(64))

        # Client computes cr = hash(cc + sc + secret)
        cr = sha256(cc + sc + secret)

        # Client sends cr and cc to peer
        self.bot.connection.privmsg(target,
            "authresponse %s %s" % (cr.hexdigest(),
                encodestring(cc).strip()))
