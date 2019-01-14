import importlib


class ReportsHandler(object):
    def __init__(self, **kwargs):
        if isinstance(kwargs["handler"], list):
            self.handlers = kwargs["handler"]
        else:
            self.handlers = [kwargs["handler"]]  # only one in list

    def handle(self, model_in):
        data_in = model_in
        for handler_str in self.handlers:
            print("Calling handler --> " + handler_str)
            m = importlib.import_module("handler." + handler_str, handler_str)
            res = m.run(data_in)  # each handler should has run function
            if res is not None:
                # the previous handler's result with push to next handler
                data_in = [res]
        # return the last handler's result
        return data_in
