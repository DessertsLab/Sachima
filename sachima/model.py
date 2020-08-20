import pandas as pd
from sachima import conf
import os
import importlib
from sachima.params import set_sql_params
from sachima.log import logger
from sachima.wrappers import timer

# from tqdm import tqdm
import io
import time
import logging
import sys
import threading
import itertools


@timer
def sql(sql, datatype):
    """
    return DataFrame
    """
    logger.info("running sql {}".format(sql))
    return pd.read_sql(sql, datatype)


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
            self.data = pd.read_excel(os.path.join(conf.get("PROJ_DIR"), dataname))
        elif datatype in ("csv", "txt"):
            self.data = pd.read_csv(os.path.join(conf.get("PROJ_DIR"), dataname))
        elif datatype in ("api",):
            api_cls = importlib.import_module("services." + dataname, package="..")
            api = api_cls.Api()
            self.data = api.data
        elif datatype in ("json",):
            self.data = pd.read_json(os.path.join(conf.get("PROJ_DIR"), dataname))
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

            self.data = _get_df(sql, datatype, dataname)


def animate(dataname, log):
    t = threading.currentThread()
    elapsed_time = 0
    for c in itertools.cycle(["|", "/", "-", "\\"]):
        if getattr(t, "Done", True):
            break
        sys.stdout.write("\r<{}> running {} {} ms\r".format(dataname, c, elapsed_time))
        sys.stdout.flush()
        time.sleep(0.1)
        elapsed_time += 100

    # log("<{}> parsing elapsed time: {} ms".format(dataname, elapsed_time))
    log("\r")
    # sys.stdout.write("\r\n Done!     ")


def _get_df(sql, datatype, dataname):
    animate_thread = threading.Thread(target=animate, args=(dataname, logger.info))
    animate_thread.daemon = True
    animate_thread.Done = False
    animate_thread.start()

    try:
        start = time.time()
        df = pd.read_sql(sql, datatype)
        consumed_time = time.time() - start

        logger.info("<{}> time: {} secs".format(dataname, consumed_time))
    except Exception as e:
        raise e
    finally:
        animate_thread.Done = True  # no matter how break the animate loop
    # logger.info("<{}> start loading data... ".format(dataname))

    # # df = pd.concat(first + [chunk for chunk in tqdm(chunks, total=200)])

    # logger.info(
    #     "<{}> loading data elapsed time: {} seconds".format(
    #         dataname, loading_data_elapsed_time
    #     )
    # )
    return df

