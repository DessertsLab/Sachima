import pandas as pd
import json
from sachima.filter_enum import FilterEnum


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
        if isinstance(copy_params[k], list):
            copy_params[k] = str(tuple(copy_params[k])).replace(",)", ")")
    return sql.format(**copy_params)


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
        return "Filter(" + self.id + ")"

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
            if isinstance(arg, dict):
                colname = arg.get("option", None)
                if isinstance(colname, str) and colname in data.columns:
                    res.update(
                        {
                            "option": data[colname]
                            .sort_values()
                            .map(lambda x: str(x))
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
        return {"columns": ["提示信息"], "dataSource": [{"提示信息": "出现错误请联系管理员"}]}

    # print(data)
    print("changing the data into json str...")
    res = {}
    df = data["data"][0]
    filters = data["filters"]

    if isinstance(df, pd.DataFrame):
        res["controls"] = [f.to_json(df) for f in filters]
        res["columns"] = df.columns.tolist()
        res["dataSource"] = json.loads(
            df.to_json(
                orient="records",
                date_format="iso",
                date_unit="s",
                force_ascii=False,
            )
        )
        print("------------------return api----------------------")
        # print("{{{{{{{{{{{{{{{{{{{")
        # print(res)
        # return json.dumps(res)
        return res
    else:
        raise TypeError("your handler should return pd.DataFrame")
