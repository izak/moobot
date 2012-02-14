#! /usr/bin/env python
#
# Hacked together from irclib example

"""A simple example bot.

The known commands are:

    stats -- Prints some channel information.
"""

from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr

class MooBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        nick = nm_to_n(e.source())
        c.privmsg(nick, "You (%s) said: %s" % (nick, e.arguments()[0]))
        self.do_command(e, e.arguments()[0], nick)

    def on_pubmsg(self, c, e):
        nick = nm_to_n(e.source())
        target = e.target()
        c.privmsg(target, "%s: You said: %s" % (nick, e.arguments()[0]))
        a = e.arguments()[0].split(":", 1)
        if len(a) > 1 and irc_lower(a[0]) == irc_lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip(), target)
        return

    def do_command(self, e, cmd, target):
        c = self.connection

        if cmd == "stats":
            for chname, chobj in self.channels.items():
                c.privmsg(target, "--- Channel statistics ---")
                c.privmsg(target, "Channel: " + chname)
                users = chobj.users()
                users.sort()
                c.privmsg(target, "Users: " + ", ".join(users))
                opers = chobj.opers()
                opers.sort()
                c.privmsg(target, "Opers: " + ", ".join(opers))
                voiced = chobj.voiced()
                voiced.sort()
                c.privmsg(target, "Voiced: " + ", ".join(voiced))
        else:
            c.privmsg(target, "Not understood: " + cmd)

def main():
    import sys
    if len(sys.argv) != 4:
        print "Usage: testbot <server[:port]> <channel> <nickname>"
        sys.exit(1)

    s = sys.argv[1].split(":", 1)
    server = s[0]
    if len(s) == 2:
        try:
            port = int(s[1])
        except ValueError:
            print "Error: Erroneous port."
            sys.exit(1)
    else:
        port = 6667
    channel = sys.argv[2]
    nickname = sys.argv[3]

    bot = MooBot(channel, nickname, server, port)
    bot.start()

if __name__ == "__main__":
    main()
