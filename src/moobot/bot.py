#! /usr/bin/env python
#
# Hacked together from irclib example

"""A simple example bot.

The known commands are:

    stats -- Prints some channel information.
"""

import traceback
from ConfigParser import ConfigParser
from ircbot import SingleServerIRCBot
from irclib import nm_to_n, nm_to_h, irc_lower, ip_numstr_to_quad, ip_quad_to_numstr
from moobot.plugins import PassiveProvider, ActiveProvider

def activate(connection, plugin):
    # Call it, then reschedule it
    plugin()
    connection.execute_delayed(plugin.period(),
                activate, (connection, plugin))

class MooBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, port, config):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.config = config
        self.passive = [plugin(self) for plugin in PassiveProvider.plugins]
        self.active = [plugin(self) for plugin in ActiveProvider.plugins]

    def process_forever(self, timeout=0.2):
        """ Override process_forever in irclib, after each iteration,
            call the active plugins. """
        while 1:
            self.process_once(timeout)
            for plugin in self.active:
                plugin()

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        nick = nm_to_n(e.source())
        self.do_command(e, e.arguments()[0], nick)

    def on_pubmsg(self, c, e):
        nick = nm_to_n(e.source())
        target = e.target()
        a = e.arguments()[0].split(":", 1)
        if len(a) > 1 and irc_lower(a[0]) == irc_lower(self.connection.get_nickname()):
            self.do_command(e, a[1].strip(), target)
        return

    def do_command(self, e, cmd, target):
        c = self.connection
        arg = cmd.split(" ")

        for plugin in self.passive:
            if arg[0] == plugin.name:
                try:
                    return plugin(target, *arg[1:])
                except:
                    tb = traceback.format_exc()
                    for l in tb.split("\n"):
                        c.privmsg(target, l)
                    return None
        c.privmsg(target, "-Not understood: " + cmd)

    def start(self):
        # Schedule active plugins
        for plugin in self.active:
            self.connection.execute_delayed(plugin.period(),
                activate, (self.connection, plugin))

        # Start it
        SingleServerIRCBot.start(self)

def main():
    import sys

    if len(sys.argv) != 2:
        print "Usage: %s configfile" % sys.argv[0]
        sys.exit(1)

    config = ConfigParser()
    config.read(sys.argv[1])

    server = config.get('server', 'host')
    port = int(config.get('server', 'port'))
    channel = config.get('server', 'channel')
    nickname = config.get('server', 'nick')

    # Load plugins
    modules = [x.strip() for x in \
        config.get('plugins', 'load').strip().split('\n')]
    for module in modules:
        __import__(module)

    bot = MooBot(channel, nickname, server, port, config)
    bot.start()

if __name__ == '__main__':
    main()
