def set_sql_params(sql, user_params, api_params):
    # test
    # sql = 'select 1 from {表} where col1 in {aaa}'
    # params = {"表": "debit_order", "aaa": [1, 2, 3]}

    # combine two dict  api_params will overwrite user_params
    params = {**user_params, **api_params}

    # convert dict to tuple for sql
    for k in params:
        if (isinstance(params[k], list)):
            params[k] = tuple(params[k])

    return sql.format(**params)


class Filter(object):
    def __init__(self, platform='superset', frontend='antd'):
        self.frontend = frontend
        self.platform = platform


if __name__ == '__main__':
    print(set_sql_params('', '', ''))
