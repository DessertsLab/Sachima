import pandas as pd


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

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Filter name should be type of string")
        setattr(self, "_name", value)

    def __repr__(self):
        return "Filter(" + self.name + ")"

    def to_json(self):
        return {"a": "b"}
