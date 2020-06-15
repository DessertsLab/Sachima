import io
import json

import pandas as pd
from sachima.filter_enum import FilterEnum
from sachima.log import logger


def delfunc(sql, e):
    buf = io.StringIO(sql)
    temp = ""
    for line in buf.readlines():
        if "{" + e + "}" in line and "-- ifnulldel" in line:
            # logger.debug("del sql line: " + line)
            pass
        elif "{" + e + "}" in line and "-- ifnulldel" not in line:
            temp += line.replace("{" + e + "}", "")
        else:
            temp += line
    return temp


def sql_format(sql, params):
    try:
        # logger.info("sql lens：" + str(len(sql)))
        return sql.format(**params)
    except KeyError as e:
        newsql = delfunc(sql, str(e).replace("'", ""))
        return sql_format(newsql, params)


def set_sql_params(sql, params):
    """
    set params to sql
    return sql str\n
    for example:
        select {colname1} from {tablename} where {colname2} = '{value}'
    """
    copy_params = {}
    copy_params.update(params)
    # convert dict to tuple for sql
    for k in params:
        logger.info(
            "set sql param {} {} type {} ".format(
                k, copy_params[k], type(copy_params[k])
            )
        )
        if isinstance(copy_params[k], list):
            if k + "0" in sql or k + "1" in sql:
                copy_params[k + "0"] = copy_params[k][0]
                copy_params[k + "1"] = copy_params[k][1]
            if len(copy_params[k]) == 0:
                copy_params[k] = [""]
            copy_params[k] = str(tuple(copy_params[k])).replace(",)", ")")
            # logger.debug("convert dict to tuple for sql: " + copy_params[k])
    finalsql = sql_format(sql, copy_params)
    logger.debug(finalsql)
    return finalsql


class Filter:
    def __init__(self, id, setter, **kw):
        """
        id: str
        setter: tuple
        """
        self.id = id
        self.setter = setter
        self.kw = kw

    def __repr__(self):
        return "Filter({!r})".format(self.id)

    def to_json(self, data):
        res = {"id": "", "props": {}}
        res.update(self.kw)
        res["id"] = self.id

        if not isinstance(data, pd.DataFrame):
            raise TypeError("pd.DataFrame expected but get {}".format(str(type(data))))

        # todo: json str from enumn tree improve
        for arg in self.setter:
            if isinstance(arg, FilterEnum.TYPE):
                res["type"] = arg.value
            if isinstance(arg, FilterEnum.PROPS.MODE):
                res["props"].update({"mode": arg.value})
            if isinstance(arg, FilterEnum.PROPS.ALLOWCLEAR):
                res["props"].update({"allowClear": arg.value})
            if isinstance(arg, FilterEnum.PROPS.SIZE):
                res["props"].update({"size": arg.value})
            if isinstance(arg, FilterEnum.PROPS.SHOWTIME):
                res["props"].update({"showTime": arg.value})
            if isinstance(arg, FilterEnum.PROPS.DEFAULTOPEN):
                res["props"].update({"defaultOpen": arg.value})
            if isinstance(arg, FilterEnum.PROPS.OPEN):
                res["props"].update({"defaultOpen": arg.value})
            if isinstance(arg, FilterEnum.PROPS.LOADING):
                res["props"].update({"loading": arg.value})
            if isinstance(arg, FilterEnum.PROPS.SHOWSEARCH):
                res["props"].update({"showSearch": arg.value})
            if isinstance(arg, dict):
                colname = arg.get("option", None)
                if isinstance(colname, str) and colname in data.columns:
                    res.update(
                        {"option": data[colname].map(lambda x: x).unique().tolist()}
                    )
                elif isinstance(colname, list):
                    res.update(arg)
                elif isinstance(colname, str):
                    res.update({"option": ["handler返回的数据没有字段名" + colname + " 请手动输入数据"]})
                    res["props"].update({"mode": "tags"})
                else:
                    res["props"].update(arg)
        return res
