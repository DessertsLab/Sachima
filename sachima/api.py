import inspect


class api(object):

    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        log_string = inspect.getfile(self.func) + " was called"
        print(log_string)

        self.publish()

        return self.func(*args)

    def publish(self):
        print('publish...................')
        pass


# class grpc(api):

#     def __init__(self, func, p1='111'):
#         self.abc = p1
#         api.__init__(self, func)

#     def publish(self):
#         print(self.abc)


# class rest(api):

#     # _showfile = 'data/1.csv'

#     def __init__(self, p1='rest api had been published to s6', *args, **kwargs):
#         self.abc = p1
#         super(rest, self).__init__(*args, **kwargs)

#     def publish(self):
#         print(self.abc)
