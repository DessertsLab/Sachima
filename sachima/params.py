import pandas as pd
import json


def set_sql_params(sql, user_params, api_params):
    # test
    # sql = 'select 1 from {表} where col1 in {aaa}'
    # params = {"表": "debit_order", "aaa": [1, 2, 3]}

    # combine two dict  api_params will overwrite user_params
    params = {**user_params, **api_params}

    # convert dict to tuple for sql
    for k in params:
        if isinstance(params[k], list):
            params[k] = tuple(params[k])

    return sql.format(**params)


class Filter:
    def __init__(self, name, setter):
        self.name = name
        for arg in setter:
            print(type(arg), arg.value)

    def __repr__(self):
        return "Filter(" + self.name + ")"

    def to_json(self):
        return {"a": "b"}


def data_wrapper(data):
    return json.dumps(
        {
            "controls": [
                {"id": "日期1", "type": "DatePicker", "props": {"size": "small"}},
                {"id": "日期2", "type": "RangePicker", "props": {"size": "small"}},
                {
                    "id": "noshoptype",
                    "type": "Select",
                    "props": {
                        "mode": "tags",
                        "allowClear": True,
                        "placeholder": "待输入",
                    },
                    "option": ["TEST", ""],
                },
                {
                    "id": "Test2",
                    "type": "Select",
                    "props": {
                        "mode": "multiple",
                        "allowClear": True,
                        "placeholder": "pls input",
                    },
                    "option": [1, 2, 3],
                },
                {
                    "id": "行业类型",
                    "type": "Select",
                    "props": {
                        "mode": "multiple",
                        "allowClear": True,
                        "placeholder": "pls input",
                    },
                    "option": ["医美", "祛痘", "其它"],
                },
                {
                    "id": "测试4",
                    "type": "Select",
                    "props": {
                        "mode": "multiple",
                        "allowClear": True,
                        "placeholder": "pls input",
                    },
                    "option": [1],
                },
                {
                    "id": "测试6",
                    "type": "Select",
                    "props": {
                        "mode": "multiple",
                        "allowClear": True,
                        "placeholder": "pls input",
                    },
                    "option": [],
                },
            ],
            "columns": ["a", "b"],
            "dataSource": [{"a": 1, "b": 2}, {"a": 3, "b": 4}],
        }
    )

