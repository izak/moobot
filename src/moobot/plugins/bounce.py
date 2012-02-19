from moobot.plugins import PassiveProvider

class BounceCheckProvider(PassiveProvider):
    """ Bounce a check to another node. The basic idea is that checking
        a service on this box involves a remote check, for example, checking
        my web server involves asking a remote host to contact it. """

    name = "bounce"
    description = "Ask another node to perform a command"

    def run(self, target, *args):
        c = self.bot.connection
        if len(args) == 0:
            c.privmsg(target, "Boing! (Hint: bounce nickname command [args]")
            return None

        if len(args) < 2:
            c.privmsg(target, "Tell me what to bounce against whom.")
            return None

        c.privmsg(args[0], *args[1:])

# TODO: Another passive provider that reacts on the returning result
