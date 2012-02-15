import os
from moobot.plugins import ActionProvider

class DiskUsageProvider(ActionProvider):
    name = "disk"
    description = "Return the Disk Usage"

    def run(self, target, *args):
        c = self.bot.connection

        f = open("/proc/mounts", "r")
        mounts = [x.split(" ")[1] for x in f.readlines()]
        f.close()

        for arg in args:
            if arg not in mounts:
                c.privmsg(target, "- %s not a mount point" % arg)
                continue

            try:
                disk = os.statvfs(arg)
            except OSError:
                c.privmsg(target, "- %s not found" % arg)
                continue

            capacity = disk.f_bsize * disk.f_blocks
            available = disk.f_bsize * disk.f_bavail
            c.privmsg(target, "+ %s %2d%%" % (arg, (available*100)/capacity))
