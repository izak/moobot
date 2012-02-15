import socket
from moobot.plugins import ActionProvider

class TCPCheckProvider(ActionProvider):
    name = "smtp"
    description = "Connect to a smtp server"

    def run(self, target, *args):
        c = self.bot.connection
        if len(args) == 0:
            c.privmsg(target, "What host should I check?")
            return None

        timeout = 30
        if len(args)>1:
            try:
                timeout = int(args[1])
            except ValueError:
                c.privmsg(target, "Timeout should be an integer value")
                return None

        port = 25
        if len(args)>2:
            try:
                port = int(args[2])
            except ValueError:
                c.privmsg(target, "port should be an integer value")
                return None

        host = args[0]
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(timeout)
            s.connect((host, port))
            if len(s.recv(1024)) == 0:
                c.privmsg(target, "- %s No Greeting" % host)
                return None
        except socket.timeout:
            c.privmsg(target, "- %s timeout" % host)
            return None
        except socket.error:
            c.privmsg(target, "- %s Could not connect" % host)
            return None

        c.privmsg(target, "+ %s" % host)
