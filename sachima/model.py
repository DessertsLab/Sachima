import pandas as pd
from sachima import conf
import os
import importlib
from sachima.params import set_sql_params
from sachima.log import logger
from tqdm import tqdm
import io
import time
import logging
import sys
import threading
import itertools


class Data:
    def __init__(self, dataname, datatype, params, prefunc):
        """
        dataname: sql filename
        datatype: db engine  or filetype in str
        """
        self.source = dataname
        self.type = datatype
        title = dataname + " | " + str(datatype)
        logger.info("=" * 12 + " " + title + " " + "=" * 12)
        if datatype in ("xls", "xlsx"):
            self.data = pd.read_excel(
                os.path.join(conf.get("PROJ_DIR"), "data", dataname)
            )
        elif datatype in ("csv", "txt"):
            self.data = pd.read_csv(
                os.path.join(conf.get("PROJ_DIR"), "data", dataname)
            )
        elif datatype in ("api",):
            api_cls = importlib.import_module("services." + dataname, package="..")
            api = api_cls.Api()
            self.data = api.data
        else:
            # read sql file from ./sqls
            str_sql = open(
                os.path.join(conf.get("PROJ_DIR"), "sqls", dataname), encoding="utf-8",
            ).read()
            sql = str_sql
            # pre process before sql loaded
            if prefunc:
                sql = prefunc(set_sql_params(str_sql, params), params)
            else:
                sql = set_sql_params(str_sql, params)

            start = time.time()
            done = False

            def animate(log):
                elapsed_time = 0
                for c in itertools.cycle(["|", "/", "-", "\\"]):
                    if done:
                        break
                    sys.stdout.write(
                        "\r<{}> parsing sql {} {} ms".format(dataname, c, elapsed_time)
                    )
                    sys.stdout.flush()
                    time.sleep(0.1)
                    elapsed_time += 100
                log("<{}> parsing elapsed time: {} ms".format(dataname, elapsed_time))
                # sys.stdout.write("\r\n Done!     ")

            t = threading.Thread(target=animate, args=(logger.info,))
            t.daemon = True
            t.start()

            chunks = pd.read_sql(sql, datatype, chunksize=100)
            done = True
            t.join()
            df = pd.DataFrame()
            logger.info("<{}> start loading data... ".format(dataname))
            for chunk in tqdm(chunks, total=200):
                df = pd.concat([df, chunk])
            loading_data_elapsed_time = time.time() - start
            logger.info(
                "<{}> loading data elapsed time: {} seconds".format(
                    dataname, loading_data_elapsed_time
                )
            )
            self.data = df
