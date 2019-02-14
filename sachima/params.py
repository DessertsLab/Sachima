import pandas as pd
import json
import io
from sachima.filter_enum import FilterEnum


def delfunc(sql, e):
    buf = io.StringIO(sql)
    temp = ""
    for line in buf.readlines():
        if "{" + e + "}" in line and "-- ifnulldel" in line:
            print("删除：" + line)
        elif "{" + e + "}" in line and "-- ifnulldel" not in line:
            temp += line.replace("{" + e + "}", "")
        else:
            temp += line
    return temp


def sql_format(sql, params):
    res = ""
    try:
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
        print(k, copy_params[k], type(copy_params[k]))
        if isinstance(copy_params[k], list):
            copy_params[k] = str(tuple(copy_params[k])).replace(",)", ")")
    # print(sql.format(**copy_params))
    finalsql = sql_format(sql, params)
    print(finalsql)
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
            raise TypeError(
                "pd.DataFrame expected but get {}".format(str(type(data)))
            )

        # todo: json str from enumn tree improve
        for arg in self.setter:
            if isinstance(arg, FilterEnum.TYPE):
                res["type"] = arg.value
            if isinstance(arg, FilterEnum.PROPS.MODE):  # bug++++
                res["props"].update({"mode": arg.value})
            if isinstance(arg, FilterEnum.PROPS.ALLOWCLEAR):
                res["props"].update({"allowClear": arg.value})
            if isinstance(arg, FilterEnum.PROPS.SIZE):
                res["props"].update({"size": arg.value})
            if isinstance(arg, FilterEnum.PROPS.SHOWTIME):
                res["props"].update({"showTime": arg.value})
            if isinstance(arg, dict):
                colname = arg.get("option", None)
                if isinstance(colname, str) and colname in data.columns:
                    res.update(
                        {
                            "option": data[colname]
                            .map(lambda x: x)
                            .unique()
                            .tolist()
                        }
                    )
                elif colname:
                    res.update(arg)
                else:
                    res["props"].update(arg)
        # print(res)
        return res


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

    # print(data)
    print("changing the data into json str...")
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
        print("------------------return api----------------------")
        return res
    else:
        raise TypeError("your handler should return pd.DataFrame")
