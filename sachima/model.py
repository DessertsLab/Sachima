import pandas as pd
from sachima import conf
import os
import importlib
from sachima.params import set_sql_params
from sachima.log import logger


class Data:
    def __init__(self, dataname, datatype, params):
        """
        dataname: sql filename
        datatype: db engine  or filetype in str
        """
        self.source = dataname
        self.type = datatype
        logger.info(dataname + str(datatype))
        if datatype in ("xls", "xlsx"):
            self.data = pd.read_excel(
                os.path.join(conf.get("PROJ_DIR"), "data", dataname)
            )
        elif datatype in ("csv", "txt"):
            self.data = pd.read_csv(
                os.path.join(conf.get("PROJ_DIR"), "data", dataname)
            )
        elif datatype in ("api",):
            api_cls = importlib.import_module(
                "services." + dataname, package=".."
            )
            api = api_cls.Api()
            self.data = api.data
        else:
            str_sql = open(
                os.path.join(conf.get("PROJ_DIR"), "sqls", dataname),
                encoding="utf-8",
            ).read()
            sql = set_sql_params(str_sql, params)
            self.data = pd.read_sql(sql, datatype)
