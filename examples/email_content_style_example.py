from sachima.send import send
from sachima.api import api
from sachima.tools import clock
from sachima.scheduler import only_in_night
from sachima.main_runner import run
from sachima.db_connects import db
from sachima.filter_enum import FilterEnum as _
from sachima.params import Filter

db = db()


def get_debit_level():
    return 1 + 1


# @only_in_night
# @clock
# @send
# @api(type='grpc', platform='superset')
def main(api_params={}):
    set_date_filter = (
        _.TYPE.ITEMSELECT,
        _.PROPS.ALLOWCLEAR.TRUE,
        _.PROPS.SIZE.SMALL,
        _.PROPS.MODE.MULTIPLE,
        _.PROPS.P.A,
        _.PROPS.P.B,
    )

    f1 = Filter("筛选字段1", setter=set_date_filter)
    f2 = Filter("筛选字段2", setter=set_date_filter)
    f3 = Filter("noshoptype", setter=set_date_filter)

    PARAM_IN = {
        "model": [("email_content_style_example.sql", db.ENGINE_MYSQL_duckchat)],
        # "handler": ["email_content_style_example", "another_handler"]
        "handler": "email_content_style_example",
        "params": {
            "noshoptype": "TEST",
            "debit_level": get_debit_level(),
            "日期": "2019-01-11",
            "行业类型": ["yimei", "qudou"],
        },
        "filters": [f1, f2, f3],
    }
    return run(PARAM_IN, api_params)


# 下拉选择 字体小  允许清除 多选


if __name__ == "__main__":
    # testing
    # res = main()
    # print(res)
    pass
