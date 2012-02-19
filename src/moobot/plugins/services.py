from moobot.plugins import PassiveProvider

class ServicesProvider(PassiveProvider):
    name = "services"
    description = "Manages a list of services on a host"

    def run(self, target, *args):
        def help():
            self.bot.connection.privmsg(target, "Usage:")
            self.bot.connection.privmsg(target, "        services list");
            self.bot.connection.privmsg(target, "        services check servicename");

        def check(service):
            name = self.bot.config.get('service:%s' % service, 'plugin')
            args = self.bot.config.get('service:%s' % service, 'args')
            args = [a.strip() for a in args.strip().split('\n')]

            plugin = self.bot.passive.get(name, None)
            if plugin is not None:
                plugin(target, *args)
            else:
                self.bot.connection.privmsg(target,
                    "Plugin %s is not enabled" % name)

        services = [x.strip() for x in \
            self.bot.config.get('services', 'services').strip().split('\n')]
        if len(args)==0:
            help()
        elif args[0] == "list":
            self.bot.connection.privmsg(target, ", ".join(services))
        elif args[0] == "check":
            if len(args) < 2:
                self.bot.connection.privmsg(target,
                    "Which service should I check?")
            else:
                check(args[1])
        else:
            help()
