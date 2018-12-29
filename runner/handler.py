import importlib


class ReportsHandler(object):
    reports_lists = []

    def __init__(self, *r_list):
        self.reports_lists = r_list

    def handle(self, model_in):
        for report in self.reports_lists:
            print(report)
            m = importlib.import_module('handler.'+report, report)
            m.run(model_in)
