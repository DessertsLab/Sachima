def set_sql_params(sql, params):
    return 'select 1 from dual'


class Filter(object):
    def __init__(self, platform='superset', frontend='antd'):
        self.frontend = frontend
        self.platform = platform
