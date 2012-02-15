from moobot.plugins import ActionProvider

class LoadAverageProvider(ActionProvider):
    name = "loadavg"
    description = "Return the load average"

    def run(self, target, *args):
        c = self.bot.connection
        f = open("/proc/loadavg", "r")
        v = f.readline().split(" ")[:3]
        f.close()
        c.privmsg(target, "+ " + " ".join(v))
