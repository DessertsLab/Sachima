import hashlib
import os
import re
import sys
import uuid
from calendar import monthrange, weekday
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

# from sachima.excel_high_light import ExcelHighLighter
from sachima.tools import Tools
from sachima import conf

# if sys.platform == "darwin":
#     BASE_FILES_PATH = "/Users/zhangmk/Desktop/alert/"
#     CONF_PATH = "/Users/zhangmk/Downloads/CODE/MEIHAO/mail/alertconf.csv"
#     OUT_PATH = BASE_FILES_PATH
# elif sys.platform == "win32":
#     BASE_FILES_PATH = "d:\\share"
#     CONF_PATH = "d:\\python_work\\reports\\alertconf.csv"
#     OUT_PATH = BASE_FILES_PATH
# elif sys.platform == "linux":
#     BASE_FILES_PATH = "/data/jiankongdata/zhangj"
#     CONF_PATH = "/data/app/reports/alertconf.csv"
#     OUT_PATH = "/data/jiankongdata/"

BASE_FILES_PATH = os.path.join(conf.get("PROJ_DIR"), "data")
OUT_PATH = BASE_FILES_PATH
CONF_PATH = os.path.join(BASE_FILES_PATH, "alertconf.csv")

BATCH_DATE = datetime.strptime(
    datetime.strftime(datetime.today(), "%Y-%m-%d"), "%Y-%m-%d"
)
TIME_LEN = 60
NEED_CHART = False

panel_data = {}


def get_md5_value(src):
    myMd5 = hashlib.md5()
    myMd5.update(src.encode("utf8"))
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest


def handle_conf(conf):
    # 打开文件
    ori = pd.read_csv(conf, index_col=None, sep=",")
    # ori = ori.replace("\xc2\xa0", " ")
    ori.replace("\xa0", " ", inplace=True, regex=True)
    ori.replace("\s+", " ", inplace=True, regex=True)
    # 判断表头第一列是不是ruleid，如果不是增加ruleid表头
    col_name = ori.columns.tolist()
    # 每一行生成md5值，放在第一列作为ruleid
    ori["ruleid"] = (
        ori[col_name]
        .drop(["ruleid"], axis=1)
        .apply(lambda x: get_md5_value("-".join(str(value) for value in x)), axis=1,)
    )
    ori.set_index(["ruleid"], inplace=True)
    ori.drop_duplicates(inplace=True)
    # 保存文件
    ori.to_csv(conf)
    return


def special_char_remove(s):
    """
    特殊字符替换处理函数
    """
    return s.replace(",", " ").replace("<", "小于").replace(">", "大于").replace("*", "_")


def time_dim_to_str(timeobj):
    """
    time_dim_to_str
    timeobj可能是任意类型的，用这个函数转换为日期格式的字符串类型
    如果是无法转换的保留字符串类型返回
    """
    if type(timeobj) == str:
        return timeobj
    elif type(timeobj) == np.int64 or type(timeobj) == int:
        return str(timeobj)
    else:
        return timeobj.strftime("%Y-%m-%d")


def date_cut(x):
    # 2017-9
    if type(x) == str and len(x) <= 7:
        temp = x.split("-")
        iyear, imonth = int(temp[0]), int(temp[1])
        sample = "-".join(
            [x, str(monthrange(iyear, imonth)[1])]
        )  # monthrange 返回 月第一天的weekday和  最后一天   join当月的最后一天
        return datetime.strptime(sample, "%Y-%m-%d")
    elif type(x) == str and len(x) > 7 and len(x) <= 10:  # 2017-08-01   20170801
        for fmt in ("%Y-%m-%d", "%Y%m%d", "%Y/%m/%d"):
            try:
                return datetime.strptime(x, fmt)
            except ValueError:
                pass
        raise ValueError("无法转换日期")
    elif type(x) == str and len(x) > 10:  # 20170701-20170801
        return datetime.strptime(x.split("-")[1], "%Y%m%d")
    else:
        return x


def clean(groupdata):
    """
    把当前时间点不完整的数据切除
    """
    # print("--------------------------------")
    # print(groupdata)
    if type(groupdata) != pd.core.frame.DataFrame:
        print("必须传入DataFrame")
        exit()
    # print('---------------')
    # print(groupdata.tail(5))
    groupdata["stattime"] = groupdata.index.map(date_cut)
    # print(groupdata.stattime)
    # print(groupdata.index)

    # edg_index = groupdata.stattime.searchsorted(datetime.now())[0]
    # # Series 上用searchsorted 返回的是ndarray
    # groupdata = groupdata[:edg_index]

    # edg_index = groupdata.stattime.searchsorted(BATCH_DATE)[0]
    # # Series 上用searchsorted 返回的是ndarray
    # groupdata = groupdata[:edg_index]

    # print('&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    # print(groupdata.tail(5))
    print(groupdata.columns)
    return groupdata


def get_last_time(groupdata):
    """
    用系统日期判断是不是存在多余的时间

    预期传入的是每个分组的数据集，一种维度组合后的dataframe
    然后根据长度判断不同的时间类型  周区间 20160829-20160904  年月 2017-12

    """
    t1 = BATCH_DATE + timedelta(days=-1)

    try:
        the_end_date_put_in = groupdata.stattime[-1]
    except:
        print("clean后没有数据，最近一期的被clean后数据变成空")
        return ""

    if the_end_date_put_in != t1:
        print(the_end_date_put_in)
        print(t1)
        print("*********最后时点非t-1，不计算")
        return ""
    else:
        return groupdata.index[-1]


def rulerun(ruleid, table, index, column, rule, param, url, f):
    """
    example: 
        ruleid=ff27a4ff5ea11f3c319670037f32316f
        table=risk.table1 
        index=dim1 dim2 td_stat_date
        column=column1 column2
        rule=R00003_multicondi
        param=< > 0.8 0.1
        url=www.google.com
        f=open("filename", "w")
    """
    df = panel_data[table]
    index = index.split(" ")  # example: d_dim1 d_dim2 td_stat_date

    # # 所有年月结合的情况
    # time_dim_possible_lists = [
    #     ("d_年份", "d_月份"),
    #     ("ty_申请年份", "tm_月份"),
    #     ("ty_放款年份", "tm_月份"),
    # ]

    # if len(index) > 1 and (index[-2], index[-1]) in time_dim_possible_lists:
    #     df["d_年月"] = df[[index[-2], index[-1]]].apply(
    #         lambda x: "-".join(str(value) for value in x), axis=1
    #     )
    #     index[-2] = "d_年月"
    #     index.pop()

    # get begin time and end time
    dt_end = max(df[index[-1]])
    if len(df[index[-1]].drop_duplicates(keep="first", inplace=False)) > TIME_LEN:
        dt_begin = (
            df[index[-1]]
            .drop_duplicates(keep="first", inplace=False)
            .sort_values()
            .iloc[-TIME_LEN]
        )
    else:
        dt_begin = min(df[index[-1]])

    # get begin time to end time range data
    df = df[(df[index[-1]] >= dt_begin) & (df[index[-1]] <= dt_end)]

    df = df.set_index(index).sort_index()
    ruletype = rule.split("_")[0]  # example： R00001_{L}阶差分值不超过{N}日移动窗口{M}个上下标准差
    eval(ruletype)(ruleid, df, table, column, param, index, url, f)


def R00001(ruleid, df, table, column, param, index, url, f):
    """
    R00001_{L}阶差分值不超过{N}日移动窗口{M}个上下标准差
    """
    s_param = param.split(" ")
    diff_deep = int(s_param[0])  # 参数按照顺序提取，配置文件中配置的时候也按照顺序   差分的次数
    window_value = int(s_param[1])  # 移动窗口长度
    std_times = float(s_param[2])  # 超过多少倍的标准差被认为是异常值
    std_top = "diff_" + str(std_times) + "times_mstd" + str(window_value)  # 上标准差的字段名
    std_bottom = (
        "diff_-" + str(std_times) + "times_mstd" + str(window_value)
    )  # 下标准差的字段名

    if len(index) > 1:
        dim_str = str(index[0:-1])  # 除了最后一个作为维度
        time_str = str(index[-1])  # 最后一个作为时间  x轴
        dimention = df.groupby(index[0:-1]).count().index  # 维度组合
    else:
        dim_str = "_"  # 为了在win上运行 不能使用星号  小于大于号等特殊字符
        time_str = str(index[0])
        dimention = ["_"]  # 除了时间没有其它维度的情况

    for groupset in dimention:
        print(
            "R00001"
            + ruleid
            + "------------正在处理分组---"
            + table
            # + filename
            + str(index)
            + "--------"
            + str(groupset)
            + "---------------正在处理分组----------------"
        )
        dt_end = ""
        dd = None

        if groupset == "_":
            dd = clean(df)
            dt_end = get_last_time(dd)
        else:
            dd = clean(df.loc[groupset])
            dt_end = get_last_time(dd)

        if type(dt_end) == str and dt_end == "":
            print("----in continue------")
            continue

        obj = dd[:dt_end][[column]]

        # if len(index) > 1:
        #     obj = df.loc[groupset][:dt_end][[column]]  # 有其它维度
        # else:
        #     obj = df[:dt_end][[column]]                # 只有时间维度

        if obj.size <= 7:  # 时间序列太短
            print("时间序列小于7 退出")
            continue

        # 差分 和上一时间的差值  通过need_diff参数控制是否需要差分， 通过diff_deep参数控制diff的阶数
        obj["diff"] = obj[column]  # 增加diff字段 初始化的时候等于原值
        i = diff_deep  # diff_deep 阶差分
        while i > 0:
            # print("进行差分操作"+str(i))
            obj["diff"] = obj["diff"].diff()
            i = i - 1

        # Moving average 移动平均数 window_value天的平均值
        obj["diff_ma" + str(window_value)] = (
            obj["diff"].rolling(window=window_value, center=False).mean()
        )
        # Moving std 移动标准差  std_times倍标准差
        obj[std_top] = (
            std_times * obj["diff"].rolling(window=window_value, center=False).std()
        )
        obj[std_bottom] = (
            -std_times * obj["diff"].rolling(window=window_value, center=False).std()
        )

        # 判断指标是否在范围内 增加向上或向下波动异常
        conditions = [
            (obj["diff"] > obj[std_top]) | (obj["diff"] < obj[std_bottom]),
            1 == 1,
        ]
        conditios_up = [(obj["diff"] > obj[std_top]), 1 == 1]
        conditios_down = [(obj["diff"] < obj[std_bottom]), 1 == 1]
        choices = [True, False]  # True代表触发了预警
        obj["res"] = np.select(conditions, choices, default=False)
        obj["up"] = np.select(conditios_up, choices, default=False)
        obj["down"] = np.select(conditios_down, choices, default=False)
        # alerttext = dim_str+"为"+str(groupset)+'的[' + column + ']的'+str(diff_deep)+'阶差分值超过' + str(window_value) + '日窗口的' + str(std_times) + '个标准差'

        if obj.loc[obj.index[-1]]["res"] == False:  # 最后一个点必须是预警点  否则不输出预警
            print("最后一个点必须是预警点  否则不输出预警")
            continue

        # 只记录最后一个点的预警
        last_dt = obj[obj["res"] == True].index[-1]
        vv = obj.loc[last_dt][column]  # 触发预警数值
        sBD = "向上波动"
        if obj.loc[last_dt]["up"] == True:
            sBD = "向上波动"
        elif obj.loc[last_dt]["up"] == False:
            sBD = "向下波动"

        alerttext = (
            special_char_remove(dim_str)
            + ","
            + special_char_remove(str(groupset))
            + ","
            + table
            + ",["
            + column
            + "],"
            + sBD
            + "异常,"
            + param
        )
        data_file = os.path.join("..", table + ".xlsx")  # 对应的数据文件 可以在excel中直接连接到源数据

        f.write(
            str(uuid.uuid1())
            + ","
            + ruleid
            + ",R00001,[波动预警],"
            + time_dim_to_str(last_dt)
            + ",["
            + time_str
            + "],"
            + alerttext
            + ","
            + Tools.special_char_remove(str(vv))
            + ","
            + ""
            + str(url)
            + ""
            + ',=HYPERLINK("'
            + data_file
            + '")'
            + ',=HYPERLINK("'
            + str(url)
            + '")'
            + "\n"
        )
        f.flush()


def R00005(ruleid, df, table, column, param, index, url, f):
    """
    R00005_绝对值{>=<}{T}
    """
    oper = param.split(" ")[0]  # >=<   大于等于小于
    value = float(param.split(" ")[1])  # 阈值

    if len(index) > 1:  # 如果index的长度是一代表只有时间维度，大于1的话取最后一个时间维度以外的维度index[0:-1]作groupby
        dim_str = str(index[0:-1])  # 其它维度
        time_str = str(index[-1])  # 时间维度
        temp = df.groupby(index[0:-1]).count().index  # 其它维度的列表,分组处理
    else:
        time_str = str(index[0])
        dim_str = "_"
        temp = ["_"]  # 除了时间没有其它维度的情况

    for groupset in temp:
        print(
            "R00005"
            + "--------ruleid:"
            + ruleid
            + "------------正在处理分组---"
            + table
            + "@"
            + str(index)
            + "--------"
            + str(groupset)
            + "----------"
        )
        dt_end = ""
        dd = None

        if groupset == "_":
            dd = clean(df)
            dt_end = get_last_time(dd)
        else:
            dd = clean(df.loc[groupset])
            dt_end = get_last_time(dd)

        # print(df.loc[groupset])
        # print(dt_end, type(dt_end) == str and dt_end == '')
        if type(dt_end) == str and dt_end == "":
            continue

        obj = dd[:dt_end][[column]]

        # std_times*obj['diff'].rolling(window=window_value, center=False).std()
        obj["thresholdvalue"] = value
        obj["-thresholdvalue"] = -1 * value

        # 判断指标是否在范围内 规则存在条件里面
        print("column: ", column)
        print("obj[column]: ", obj[column])
        if oper == ">":
            conditions = [abs(obj[column]) > obj["thresholdvalue"], 1 == 1]
            oper_str = "大于"
        elif oper == "<":
            conditions = [abs(obj[column]) < obj["thresholdvalue"], 1 == 1]
            oper_str = "小于"
        elif oper == "=":
            conditions = [abs(obj[column]) == obj["thresholdvalue"], 1 == 1]
            oper_str = "等于"

        # conditions = eval(
        #     "[abs(obj['" + column + "']) " + oper + " obj['thresholdvalue'], 1 == 1]"
        # )

        # print(con)

        # if oper == ">":
        #     oper_str = "大于"
        # elif oper == "<":
        #     oper_str = "小于"
        # elif oper == "=":
        #     oper_str = "等于"

        choices = [True, False]
        obj["res"] = np.select(conditions, choices, default=False)

        # a = obj[obj['res'] == True].index

        alerttext = (
            special_char_remove(dim_str)
            + ","
            + special_char_remove(str(groupset))
            + ","
            + table
            + ",["
            + column
            + "],绝对值"
            + oper_str
            + "阈值,"
            + str(value)
        )

        if (
            obj.loc[obj.index[-1]]["res"] == False
        ):  # 最后一个点必须是预警点  否则不输出预警  不能用is 必须 == 会有bug
            continue

        # print(obj[obj['res'] == True].index)
        last_dt = obj[obj["res"] == True].index[-1]
        vv = obj.loc[last_dt][column]
        data_file = os.path.join("..", table + ".xlsx")
        # print('---writing....--')
        f.write(
            str(uuid.uuid1())
            + ","
            + ruleid
            + ",R00005,[高限预警],"
            + time_dim_to_str(last_dt)
            + ",["
            + time_str
            + "],"
            + alerttext
            + ","
            + Tools.special_char_remove(str(vv))
            + ","
            + ""
            + str(url)
            + ""
            + ',=HYPERLINK("'
            + data_file
            + '")'
            + ',=HYPERLINK("'
            + str(url)
            + '")'
            + "\n"
        )
        f.flush()


def R00003(ruleid, df, table, column, param, index, url, f):
    """
    R00003 多条件规则匹配    Y,业务表汇总.商户周申请量,d_商户名称 tw2_周区间,申请量 申请通过率,R00002_$1{>=<}{T}AND$2{>=<}{M},> 10 < 0.25,,
    """
    column_lists = column.split(" ")
    param_lists = param.split(" ")
    print(param_lists)
    l = len(column_lists)
    oper_lists = param_lists[:l]
    value_lists = param_lists[l:]
    value_lists = [Tools.maybe_float(v) for v in value_lists]

    # print(column_lists)
    # print(oper_lists)
    # print(value_lists)

    if len(column_lists) == len(oper_lists) == len(value_lists):
        pass
    else:
        print("请输入匹配的字段参数和值，按照一个空格分割,这条规则将不会执行：" + ruleid)
        return 0

    if len(index) > 1:  # 如果index的长度是一代表只有时间维度，大于1的话取最后一个时间维度以外的维度idx[0:-1]作groupby
        dim_str = str(index[0:-1])  # 其它维度
        time_str = str(index[-1])  # 时间维度
        dimention = df.groupby(index[0:-1]).count().index  # 其它维度的列表,分组处理
    else:
        time_str = str(index[0])
        dim_str = "_"
        dimention = ["_"]  # 除了时间没有其它维度的情况

    for groupset in dimention:
        print(
            "R00003"
            + ruleid
            + "------------正在处理分组----"
            + table
            + str(index)
            + "-------"
            + str(groupset)
            + "---------------正在处理分组----------------"
        )
        dt_end = ""
        dd = None

        if groupset == "_":
            dd = clean(df)
            dt_end = get_last_time(dd)
        else:
            dd = clean(df.loc[groupset])
            dt_end = get_last_time(dd)
            # print("@@@@@@@@@@@@@@@@@@@@@@@@")
            # print(dt_end)

        if type(dt_end) == str and dt_end == "":
            continue

        obj = dd[:dt_end][list(set(column_lists))]
        # if len(index) > 1:
        #     obj = df.loc[groupset][:dt_end][column_lists]
        # else:
        #     obj = df[:dt_end][column_lists]

        # c 字段   v 预警线   o 操作
        c_markers_lists = []
        for c, v, o in zip(column_lists, value_lists, oper_lists):
            keyname = c + o + str(v)  # 字段 操作符 和值形成唯一的keyname 形成新的列
            print(keyname)
            # print(obj[c])
            # print(obj[keyname + "_thresholdvalue"])
            # 把预警线放在一个字段
            obj[keyname + "_thresholdvalue"] = v
            # 条件构造
            # print(c)
            obj[keyname + "markers"] = Tools.get_truth(
                obj[c], o, obj[keyname + "_thresholdvalue"]
            )
            c_markers_lists.append(keyname + "markers")

        obj["res"] = obj[c_markers_lists].all(axis=1)  # 必须满足所有的条件才触发预警

        alerttext = (
            special_char_remove(dim_str)
            + ","
            + special_char_remove(str(groupset))
            + ","
            + table
            + ","
            + Tools.special_char_remove(str(column_lists))
            + ","
            + Tools.special_char_remove(str(oper_lists))
            + ","
            + Tools.special_char_remove(str(value_lists))
        )

        if obj.loc[obj.index[-1]]["res"] == False:  # 最后一个点必须是预警点  否则不输出预警
            continue

        last_dt = obj[obj["res"] == True].index[-1]
        vv = list(obj.loc[last_dt][column_lists])
        # data_file = os.path.join("..", table + ".xlsx")
        # "预警编号,规则编号,触发规则,规则类型,日期,日期类型,维度名称,维度值,表格,字段,描述,参数,值,图,数据,url" + "\n"
        f.write(
            str(uuid.uuid1())
            + ","
            + ruleid
            + ",R00003,[多条件预警],"
            + time_dim_to_str(last_dt)
            + ",["
            + time_str
            + "],"
            + alerttext
            + ","
            + Tools.special_char_remove(str(vv))
            + ","
            + str(url)
            + ',=HYPERLINK("'
            + str(url)
            + '")'
            + "\n"
        )
        f.flush()


def get(days=1, conf_path=CONF_PATH):
    """
    get alert out put
    """
    for d in range(0, days):
        BATCH_DATE = datetime.strptime(
            datetime.strftime(datetime.today(), "%Y-%m-%d"), "%Y-%m-%d"
        ) + timedelta(days=-d)

        # read alert conf file
        conf = pd.read_csv(conf_path, index_col=None, sep=",")
        # you can config active==N in config file to disable the alert rule
        conf = conf[conf["active"] == "Y"]

        # the path store results
        last_path = os.path.join(
            OUT_PATH, "lastest_alerts" + datetime.strftime(BATCH_DATE, "%Y%m%d"),
        )

        if not os.path.exists(last_path):
            os.makedirs(last_path)

        csv_file_name = os.path.join(
            last_path, "alertlist" + datetime.strftime(BATCH_DATE, "%Y%m%d") + ".csv",
        )

        f_last_alerts = open(csv_file_name, "w")
        f_last_alerts.write(
            "预警编号,规则编号,触发规则,规则类型,日期,日期类型,维度名称,维度值,表格,字段,描述,参数,值,图,数据,url" + "\n"
        )
        f_last_alerts.flush()

        for index, row in conf.iterrows():
            rulerun(
                row["ruleid"],
                row["table"],
                row["index"],
                row["column"],
                row["rule"],
                row["param"],
                row["url"],
                f_last_alerts,
            )

        f_last_alerts.close()

        # 转换成excel并格式化
        # filename = '/Users/zhangmk/Downloads/监控指标制作/lastest_alerts20180523/alertlist20180521.csv'

        # excel的处理不该在alert中做 alert应该负责规则处理  统一生成df后由调用方处理
        # ehl = ExcelHighLighter(
        #     csv_file_name,
        #     highcols=["触发规则", "规则类型", "日期类型", "维度名称", "表格", "字段"],
        #     hide=["A", "B", "N", "O"],
        #     colfilter=True,
        # )
        # ehl.to_excel()
        return pd.read_csv(csv_file_name)


def add(name, df):
    """
    add df to global panel_data 
    name: path.filename
    df: input pandas Dataframe
    """
    panel_data[name] = df

