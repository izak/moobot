from moobot.plugins import ActionProvider

# Common plugins, serves as an example of how to do it
class StatsProvider(ActionProvider):
    name = "stats"
    description = "Provide some stats on channel usage"

    def run(self, target, *args):
        c = self.bot.connection
        for chname, chobj in self.bot.channels.items():
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
