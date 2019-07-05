from nameko.rpc import rpc, RpcProxy
import importlib
import os
import numpy as np
import pandas as pd
import json

from sachima.log import logger
from sachima.cache import RedisClient
from sachima.tools import Tools


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
    # data["link"]
    print(data)
    if not data:
        return {
            "columns": [{"title": "提示信息", "dataIndex": "提示信息", "key": "提示信息"}],
            "dataSource": [{"提示信息": "服务器数据出现错误请联系管理员"}],
        }

    logger.info("data into json str...")
    res = {}
    df = data["data"][0]
    filters = data["filters"]
    links = data.get("links", {})

    if isinstance(df, pd.DataFrame):
        res["controls"] = [f.to_json(df) for f in filters]
        res["columns"] = [
            {
                "title": x,
                "dataIndex": x,
                "key": x,
                "render": {"action": links[x]},
            }
            if x in links
            else {"title": x, "dataIndex": x, "key": x}
            for x in df.columns
        ]
        # for colname in links:
        #     res["columns"][colname]["render"] = {
        #         "action": "http://www.baidu.com/s?wd="
        #     }
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
        """
        todo: 加入缓存功能
        1.缓存出故障通知但不影响应用返回 done
        2.让调用方可以强制更新缓存  done
        3.批量刷新缓存（时间间隔，表格配置，不配的默认不刷新）
        4.晚间定时全部刷新
        5.设置最大内存，缓存淘汰策略
        """
        logger.info("=" * 50)
        logger.info(params)
        logger.info("=" * 50)
        need_fallback = False
        force_flash = params.get("isForce", 0)  # 0 使用缓存  1 不使用缓存
        params.pop("isForce", None)  # 把请求中控制是否强制刷新的flag去掉
        req = json.dumps(params)
        req_md5 = Tools.get_md5_value(req)

        try:
            conn = RedisClient().conn
            ret = conn.hget("sachima_results", req_md5)
            conn.zincrby("sachima_board", 1, req_md5)  # 监控访问次数

        except:
            # print(TypeError, ValueError)
            logger.info("cache exception, fallbacking..... will not use cache")
            need_fallback = True  # 缓存出现异常，需要降级回退处理

        # 不需要降级并且有返回值并且前端没有要求强制刷新并且命中缓存
        if not need_fallback and not force_flash and ret:
            # cache hit
            logger.debug("cache hit")
            return json.loads(ret)
        else:
            # cache miss
            logger.debug("cache miss")
            logger.debug("call service: " + params.get("name"))
            m = importlib.import_module(params.get("name"))
            res = data_wrapper(m.main(params))

            if not need_fallback:
                conn.hset("sachima_req", req_md5, req)
                conn.hset("sachima_results", req_md5, json.dumps(res))  # 更新缓存
        return res

    @rpc
    def writecache(self, name, value, conn=RedisClient().conn):
        logger.debug("writecache to: " + name)
        conn.rpush(
            name,
            json.dumps(value, indent=2, ensure_ascii=False).encode("utf-8"),
        )

    @rpc
    def popcache(self, name, conn=RedisClient().conn):
        logger.debug("lpopcache: " + name)
        return conn.lpop(name)
