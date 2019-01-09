import importlib


class ReportsHandler(object):
    def __init__(self, **kwargs):
        if isinstance(kwargs['handler'], list):
            self.reports_lists = kwargs['handler']
        else:
            self.reports_lists = [kwargs['handler']]

    def handle(self, model_in):
        data_in = model_in
        for report in self.reports_lists:
            print(report)
            m = importlib.import_module('handler.'+report, report)
            res = m.run(data_in)
            if res is not None:
                data_in = [res]
        return data_in
