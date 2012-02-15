from moobot.plugins import ActionProvider

class LoadAverageProvider(ActionProvider):
    name = "loadavg"
    description = "Return the load average"

    def run(self, bot, target, *args):
        c = bot.connection
        f = open("/proc/loadavg", "r")
        v = f.readline().split(" ")[:3]
        f.close()
        c.privmsg(target, "+ " + " ".join(v))
