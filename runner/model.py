import pandas as pd
import os
import importlib


class Data:
    def __init__(self, dataname, datatype):
        '''
        dataname: sql filename
        datatype: db engine  or filetype in str
        '''
        self.source = dataname
        self.type = datatype
        print(dataname + "------------" + str(datatype))
        if datatype in ('xls', 'xlsx'):
            self.data = pd.read_excel(
                os.path.join(
                    os.path.dirname(__file__), '..', 'data', dataname))
        elif datatype in ('csv', 'txt'):
            self.data = pd.read_csv(
                os.path.join(
                    os.path.dirname(__file__), '..', 'data', dataname))
        elif datatype in ('api', ):
            api_cls = importlib.import_module(
                'services.' + dataname, package='..')
            api = api_cls.Api()
            self.data = api.data
        else:
            self.data = pd.read_sql(
                open(
                    os.path.join(
                        os.path.dirname(__file__), '..', 'sqls', dataname),
                    encoding='utf-8').read(), datatype)
