from sachima.send import send
from sachima.api import api
from sachima.tools import clock
from sachima.scheduler import only_in_night
from sachima.main_runner import run
from sachima.filter_enum import FilterEnum as _
from sachima.params import Filter

from services.db_connects import db

db = db()


def get_debit_level():
    return 1 + 1


def get_option_cola():
    direcs = ["东", "南", "西", "北"]
    return direcs


# @only_in_night
# @clock
# @send
# @api(type='grpc', platform='superset')
def main(api_params={}):
    s12 = (
        _.TYPE.ITEMSELECT,
        _.PROPS.ALLOWCLEAR.TRUE,
        _.PROPS.MODE.TAGS,
        {"option": "行业"},
    )

    qishu_set = (
        _.TYPE.ITEMSELECT,
        _.PROPS.ALLOWCLEAR.TRUE,
        _.PROPS.MODE.TAGS,
        {"option": "期数"},
    )

    s13 = (
        _.TYPE.ITEMSELECT,
        _.PROPS.ALLOWCLEAR.TRUE,
        _.PROPS.MODE.TAGS,
        {"option": "所属商户"},
    )

    set_data = (_.TYPE.DATE, _.PROPS.ALLOWCLEAR.TRUE)

    set_lines = (
        _.TYPE.ITEMSELECT,
        _.PROPS.ALLOWCLEAR.TRUE,
        {"option": list(range(0, 200, 20))},
    )

    jjsj = Filter("进件时间", setter=set_data)
    rq = Filter("日期", setter=set_data)
    hy = Filter("行业", setter=s12)
    noshoptype = Filter("noshoptype", setter=s12)
    f5 = Filter("期数", setter=qishu_set)
    yourlines = Filter("行数", setter=set_lines)
    sssh = Filter("所属商户", setter=s13)

    PARAM_IN = {
        "model": [
            ("email_content_style_example.sql", db.ENGINE_MYSQL_duckchat)
        ],
        "handler": ["email_content_style_example", "another_handler"],
        # "handler": "email_content_style_example",
        "params": {
            "noshoptype": "TEST",
            "debit_level": get_debit_level(),
            "日期": "2019-01-11",
            "进件时间": "",
            "排除行业": ["行业1", "行业2"],
            "行数": 3,
        },
        "filters": [jjsj, rq, hy, noshoptype, f5, yourlines, sssh],
    }
    return run(PARAM_IN, api_params)


if __name__ == "__main__":
    # testing
    res = main()
    print(res)
    # pass
