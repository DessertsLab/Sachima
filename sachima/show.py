import inspect


class show(object):

    # _showfile = 'data/1.csv'

    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        print(args)
        log_string = inspect.getfile(self.func) + " was called"
        print(log_string)
        # with open(self._showfile, 'r') as f:
        #     print(f.readlines())

        self.notify

        return self.func(*args)

    def notify(self):
        pass
