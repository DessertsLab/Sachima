import pandas as pd
import json
from sachima.filter_enum import FilterEnum


def set_sql_params(sql, params):
    """
    set sql params from user_params and api_params to sql
    return sql str\n
    for example:
        select {colname1} from {tablename} where {colname2} = '{value}'
    """

    # combine two dict  api_params will overwrite user_params
    # params = {**user_params, **api_params}

    # convert dict to tuple for sql
    for k in params:
        if isinstance(params[k], list):
            params[k] = tuple(params[k])
    print("#" * 40)
    print(params)
    return sql.format(**params)


class Filter:
    def __init__(self, id, setter):
        """
        id: str
        setter: tuple
        """
        self.id = id
        self.setter = setter

    def __repr__(self):
        return "Filter(" + self.id + ")"

    def to_json(self):
        res = {}
        res["id"] = self.id

        # todo: json str from enumn tree improve
        for arg in self.setter:
            print(type(arg))
            if isinstance(arg, FilterEnum.TYPE):
                res["type"] = arg.value
            if isinstance(arg, FilterEnum.PROPS.MODE):  # bug++++
                res.update({"props": {"mode": arg.value}})
            if isinstance(arg, FilterEnum.PROPS.ALLOWCLEAR):
                res.update({"props": {"allowclear": arg.value}})
            if isinstance(arg, FilterEnum.PROPS.SIZE):
                res.update({"props": {"size": arg.value}})
            if isinstance(arg, dict):
                res.update(arg)

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
    print(data)
    print("changing the data into json str...")
    res = {}
    df = data["data"][0]
    # check and change index to columns
    # df.reset_index(level=0, inplace=True)

    filters = data["filters"]

    if isinstance(df, pd.DataFrame):
        res["controls"] = [f.to_json() for f in filters]
        res["columns"] = df.columns.tolist()
        res["dataSource"] = json.loads(
            df.to_json(
                orient="records", date_format="iso", date_unit="s", force_ascii=False
            )
        )
        return json.dumps(res)
    else:
        raise TypeError("your handler should return pd.DataFrame")
