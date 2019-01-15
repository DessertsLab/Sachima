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
    # convert dict to tuple for sql
    for k in params:
        if isinstance(params[k], list):
            params[k] = tuple(params[k])
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

    def to_json(self, data):
        res = {"id": "", "props": {}}
        res["id"] = self.id

        if not isinstance(data, pd.DataFrame):
            raise TypeError(
                "expect get pd.DataFrame type but get {}".format(str(type(data)))
            )

        # todo: json str from enumn tree improve
        for arg in self.setter:
            print(type(arg))
            if isinstance(arg, FilterEnum.TYPE):
                res["type"] = arg.value
            if isinstance(arg, FilterEnum.PROPS.MODE):  # bug++++
                print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
                res["props"].update({"mode": arg.value})
                print(res)
            if isinstance(arg, FilterEnum.PROPS.ALLOWCLEAR):
                res["props"].update({"allowclear": arg.value})
            if isinstance(arg, FilterEnum.PROPS.SIZE):
                res["props"].update({"size": arg.value})
            if isinstance(arg, dict):
                colname = arg.get("option", None)
                if isinstance(colname, str) and colname in data.columns:
                    res.update(
                        {
                            "option": data[colname]
                            .unique()
                            .map(lambda x: str(x))
                            .tolist()
                        }
                    )
                else:
                    res["props"].update(arg)
        print(res)
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
    filters = data["filters"]

    if isinstance(df, pd.DataFrame):
        res["controls"] = [f.to_json(df) for f in filters]
        res["columns"] = df.columns.tolist()
        res["dataSource"] = json.loads(
            df.to_json(
                orient="records", date_format="iso", date_unit="s", force_ascii=False
            )
        )
        print("-----------return api-------------")
        print(res)
        return json.dumps(res)
    else:
        raise TypeError("your handler should return pd.DataFrame")
