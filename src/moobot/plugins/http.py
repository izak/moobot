import urllib2
import socket
from moobot.plugins import ActionProvider

class HTTPCheckProvider(ActionProvider):
    name = "http"
    description = "Fetch an url"

    def run(self, target, *args):
        c = self.bot.connection
        if len(args) == 0:
            c.privmsg(target, "What url should I check?")
            return None

        timeout = 30
        if len(args)>1:
            try:
                timeout = int(args[1])
            except ValueError:
                c.privmsg(target, "Timeout should be an integer value")
                return None

        url = args[0]
        try:
            urllib2.urlopen(url, timeout = timeout)
        except urllib2.URLError, e:
            if isinstance(e.reason, socket.timeout):
                c.privmsg(target, "- %s timeout" % url)
            else:
                c.privmsg(target, "- %s Could not fetch" % url)
            return None

        c.privmsg(target, "+ %s" % url)
