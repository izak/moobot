class PluginMount(type):
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls.plugins = []
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            cls.plugins.append(cls)

class PassiveProvider(object):
    """
    Actions that fire when someone talks to us. Needs these attributes:

    name: our name, we react when a line starts with this
    description: What do we do
    run: A callable that does the deed
    """
    __metaclass__ = PluginMount

    def __init__(self, bot):
        self.bot = bot

    def __call__(self, target, *args):
        """ target is who initiated the command. """
        return self.run(target, *args)

class ActiveProvider(object):
    """ An action that fires periodically and does something, we need:
    run: a callable that does the deed
    period: how often should this run
    """
    __metaclass__ = PluginMount

    def __init__(self, bot):
        self.bot = bot

    def period(self):
        return 5

    def __call__(self):
        return self.run()

class InitProvider(object):
    """ Actions executed once, right after joining the channel.
        run: a callable
    """
    __metaclass__ = PluginMount

    def __init__(self, bot):
        self.bot = bot

    def __call__(self):
        return self.run()

class JoinActionProvider(object):
    """ Actions executed when someone joins. """
    __metaclass__ = PluginMount

    def __init__(self, bot):
        self.bot = bot

    def __call__(self, nick):
        return self.run(nick)

class LeaveActionProvider(object):
    """ Actions executed when someone leaves. """
    __metaclass__ = PluginMount

    def __init__(self, bot):
        self.bot = bot

    def __call__(self, nick):
        return self.run(nick)
