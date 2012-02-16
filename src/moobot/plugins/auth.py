from random import getrandbits
from struct import pack
from hashlib import sha256
from base64 import encodestring
from moobot.plugins import PassiveProvider

class AuthProvider(PassiveProvider):
    name = "auth"
    description = "Respond to authentication challenges"

    def run(self, target, *args):
        secret = '%08s' % (self.bot.config.get('auth', 'secret')[:8],)

        if len(args) < 1:
            c.privmsg(target, "huh?")

        # Server sends a unique challenge value sc to the client
        sc = args[0]

        # Client generates unique challenge value cc
        cc = pack('>Q', getrandbits(64))

        # Client computes cr = hash(cc + sc + secret)
        cr = sha256(cc + sc + secret)

        # Client sends cr and cc to server
        self.bot.connection.privmsg(target,
            "%s %s" % (cr.hexdigest(), encodestring(cc).strip()))
