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


def get_option_cola():
    direcs = ["东", "南", "西", "北"]
    return direcs


# @only_in_night
# @clock
# @send
# @api(type='grpc', platform='superset')
def main(api_params={}):
    # 下拉选择 字体小  允许清除 多选
    """
    # option 第一种情况
        如果 Filter的id和 返回数据的某一列相同 返回唯一值 在pandas中获取 优先级最低
    # option 第二种情况
        用户自定义sql 输出列表 {"option": "selct distinct industry from shop_basic_info"}/{"option": "r0001_option_col1.sql"},
    # option 第三种情况
        用户自定义函数 输出列表 {"option": ["option1", "option2", "option3"]} / {"option": get_option_cola()},
    """
    s1 = (
        _.TYPE.ITEMSELECT,
        _.PROPS.ALLOWCLEAR.TRUE,
        _.PROPS.MODE.TAGS,
        {"placeholder": "#请输入"},
        {"option": ["option1", "option2", "option3"]},
    )

    s11 = (
        _.TYPE.ITEMSELECT,
        _.PROPS.ALLOWCLEAR.TRUE,
        _.PROPS.MODE.TAGS,
        {"option": get_option_cola()},
    )

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

    # set_data_range = (
    #     _.TYPE.DATERANGE,
    #     _.PROPS.ALLOWCLEAR.TRUE,
    #     {"props": {"placeholder": "#请输入"}},
    # )

    jjsj = Filter("进件时间", setter=set_data)
    rq = Filter("日期", setter=set_data)
    hy = Filter("行业", setter=s12)
    noshoptype = Filter("noshoptype", setter=s12)
    f5 = Filter("期数", setter=qishu_set)
    yourlines = Filter("行数", setter=set_lines)
    sssh = Filter("所属商户", setter=s13)

    PARAM_IN = {
        "model": [("email_content_style_example.sql", db.ENGINE_MYSQL_duckchat)],
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
