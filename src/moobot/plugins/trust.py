from random import getrandbits
from struct import pack
from hashlib import sha256
from base64 import encodestring, decodestring
from moobot.plugins import InitProvider, PassiveProvider
from moobot.plugins import JoinActionProvider, LeaveActionProvider

challenges = {}
trusted = {}

def challenge(bot, peer):
    # We send a unique challenge value sc to the peer
    sc = encodestring(pack('>Q', getrandbits(64))).strip()
    challenges[peer] = sc
    bot.connection.privmsg(peer, "auth %s" % sc)

class Challenger(InitProvider):

    def __init__(self, bot):
        self.bot = bot

    def run(self):
        peers = [x.strip() for x in \
            self.bot.config.get('trust', 'peers').strip().split('\n')]

        for peer in peers:
            challenge(self.bot, peer)

class Verifier(PassiveProvider):
    name = "authresponse"
    description = "Parses the auth response, check that it is correct"

    def run(self, target, *args):
        secret = '%08s' % (self.bot.config.get('trust', 'secret')[:8],)

        if len(args) < 2:
            self.bot.connection.privmsg(target, "huh?")
            return None

        sc = challenges.get(target, None)
        if sc is None:
            self.bot.connection.privmsg(target, "I didn't challenge you!")
            return None

        cr, cc = args[:2]

        if sha256(decodestring(cc) + sc + secret).hexdigest() == cr:
            trusted[target] = None

class QueryTrust(PassiveProvider):
    name = "trust"
    description = "Do we trust this peer?"

    def run(self, target, *args):
        if len(args) < 1:
            self.bot.connection.privmsg(target, "Trust nobody?")
            return None

        if args[0] in trusted:
            self.bot.connection.privmsg(target, "Yes, I trust %s" % args[0])
        else:
            self.bot.connection.privmsg(target, "No, I distrust %s" % args[0])

class TrustOnJoin(JoinActionProvider):
    def run(self, nick):
        peers = [x.strip() for x in \
            self.bot.config.get('trust', 'peers').strip().split('\n')]

        # If someone we have a potential trust relationship with has just
        # joined, distrust him initially and challenge
        if nick in peers:
            if nick in trusted:
                del(trusted[nick])
            challenge(self.bot, nick)

class DistrustOnLeave(LeaveActionProvider):
    def run(self, nick):
        if nick in trusted:
            del(trusted[nick])
