import importlib
from sachima.log import logger


class ReportsHandler(object):
    def __init__(self, **kwargs):
        if isinstance(kwargs["handler"], list):
            self.handlers = kwargs["handler"]
        else:
            self.handlers = [kwargs["handler"]]  # only one in list

    def handle(self, model_in, params):
        data_in = model_in
        for handler in self.handlers:
            logger.info("Call handler: " + str(handler))
            m = handler
            if isinstance(handler,str):
                m = importlib.import_module("handler." + handler, handler)
                m = importlib.reload(m)
                # each handler should has run function
            res = m.run(data_in, params)
            if res is not None:
                # the previous handler's result with push to next handler
                data_in = [res]
        # return the last handler's result
        return data_in
