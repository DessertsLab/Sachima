from nameko.rpc import rpc, RpcProxy
import importlib
import os
import numpy as np
import pandas as pd
import json

from sachima.log import logger


def data_wrapper(data):
    """
    data: dict
    return: json str
    return json str to api for frontend \n
    for example:
        antd
    """
    # data["data"]
    # data["filters"]
    if not data:
        return {
            "columns": ["提示信息"],
            "dataSource": [{"提示信息": "服务器数据出现错误请联系管理员"}],
        }

    logger.info("data into json str...")
    res = {}
    df = data["data"][0]
    filters = data["filters"]

    if isinstance(df, pd.DataFrame):
        res["controls"] = [f.to_json(df) for f in filters]
        res["columns"] = df.columns.tolist()
        df = df.applymap(str)
        res["dataSource"] = json.loads(
            df.to_json(
                orient="records",
                date_format="iso",
                date_unit="s",
                force_ascii=False,
            )
        )
        logger.debug("res dataSource lens: " + str(len(res["dataSource"])))
        return res
    else:
        raise TypeError("your handler should return pd.DataFrame")


class Data(object):
    name = "data"

    @rpc
    def get_report(self, params):
        logger.debug("call rpc service: " + params["name"])
        m = importlib.import_module(params["name"])
        return data_wrapper(m.main(params))
