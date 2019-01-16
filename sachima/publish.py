class Publisher(object):
    @classmethod
    def to(cls, platform, name):
        print("publish service {} to {}".format(name, platform))
        pass
