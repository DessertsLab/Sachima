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


class DummyTqdmFile(object):
    """ Dummy file-like that will write to tqdm
    https://github.com/tqdm/tqdm/issues/313
    """

    file = None

    def __init__(self, file):
        self.file = file

    def write(self, x):
        # Avoid print() second call (useless \n)
        # if len(x.rstrip()) > 0:
        tqdm.write(x)
        # self.buf = buf.strip("\r\n\t ")

    def flush(self):
        return getattr(self.file, "flush", lambda: None)()


class Data:
    def __init__(self, dataname, datatype, params, prefunc):
        """
        dataname: sql filename
        datatype: db engine  or filetype in str
        """
        self.source = dataname
        self.type = datatype
        logger.info("Sql file name: " + dataname + " Datatype: " + str(datatype))
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
            logger.info("=" * 12 + dataname + "=" * 12)
            # tqdm.pandas()
            start = time.time()
            done = False

            def animate():
                for c in itertools.cycle(["|", "/", "-", "\\"]):
                    if done:
                        break
                    sys.stdout.write("\rparsing sql " + c)
                    sys.stdout.flush()
                    time.sleep(0.1)
                sys.stdout.write("\rDone!     ")

            t = threading.Thread(target=animate)
            t.daemon = True
            t.start()
            chunks = pd.read_sql(sql, datatype, chunksize=100)
            done = True
            df = pd.DataFrame()
            logging.basicConfig(level=logging.DEBUG, stream=DummyTqdmFile(sys.stderr))
            log = logging.getLogger(__name__)
            for chunk in tqdm(chunks, total=200):
                df = pd.concat([df, chunk])
            elapsed_time = time.time() - start
            log.info("{} elapsed_time: {} seconds".format(dataname, elapsed_time))
            self.data = df
