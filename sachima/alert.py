import hashlib
import os
import re
import sys
import uuid
from calendar import monthrange, weekday
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

from sachima.tools import Tools
from sachima import conf

BASE_FILES_PATH = os.path.join(conf.get("PROJ_DIR"), "data")
OUT_PATH = BASE_FILES_PATH
CONF_PATH = os.path.join(BASE_FILES_PATH, "alertconf.csv")

BATCH_DATE = datetime.strptime(
    datetime.strftime(datetime.today(), "%Y-%m-%d"), "%Y-%m-%d"
)
TIME_LEN = 60
NEED_CHART = False

panel_data = {}


def handle_conf(conf):
    """
    Handle config file by
    1. Remove special whitespace
    2. Drop duplicate rules
    3. Add ruleid as first column

    ps: This function will modify the conf file inplace
    """
    # Open conf file
    ori = pd.read_csv(conf, index_col=None, sep=",")

    # Remove special whitespace
    ori.replace("\xa0", " ", inplace=True, regex=True)
    ori.replace("\s+", " ", inplace=True, regex=True)

    # Column names
    col_name = ori.columns.tolist()

    # Generate md5 value for each row and put it in the first column as ruleid
    ori["ruleid"] = (
        ori[col_name]
        .drop(["ruleid"], axis=1)
        .apply(
            lambda x: Tools.get_md5_value("-".join(str(value) for value in x)), axis=1,
        )
    )
    ori.set_index(["ruleid"], inplace=True)
    ori.drop_duplicates(inplace=True)

    # Save modified conf file
    ori.to_csv(conf)


def date_cut(x):
    """
    date_cut converts the incoming string date into datetime.datetime date type after processing
    example:
    2017-9 -> 2017-09-30 00:00:00
    2017-09-03 -> 2017-09-03 00:00:00
    20170701-20170801 -> 2017-08-01 00:00:00
    """
    if type(x) == str and len(x) <= 7:
        temp = x.split("-")
        iyear, imonth = int(temp[0]), int(temp[1])
        # str(monthrange(iyear, imonth)[1] the last day of the month
        sample = "-".join([x, str(monthrange(iyear, imonth)[1])])
        return datetime.strptime(sample, "%Y-%m-%d")
    elif type(x) == str and len(x) > 7 and len(x) <= 10:  # 2017-08-01   20170801
        for fmt in ("%Y-%m-%d", "%Y%m%d", "%Y/%m/%d"):
            try:
                return datetime.strptime(x, fmt)
            except ValueError:
                pass
        raise ValueError("Could not convert date")
    elif type(x) == str and len(x) > 10:  # 20170701-20170801
        return datetime.strptime(x.split("-")[1], "%Y%m%d")
    else:
        return x


def clean(groupdata):
    """
    Cut out incomplete data at the current time point
    """
    if type(groupdata) != pd.core.frame.DataFrame:
        raise ("DataFrame must be passed in")
    groupdata["stattime"] = groupdata.index.map(date_cut)
    return groupdata


def get_last_time(groupdata):
    """
    Use the system date to determine if there is excess time

    The expected incoming data set is each grouped data set, a dataframe after a combination of dimensions
    Then judge the different time types according to the length Weekly interval 20160829-20160904 Month 2017-12

    """
    t1 = BATCH_DATE + timedelta(days=-1)

    try:
        the_end_date_put_in = groupdata.stattime[-1]
    except:
        print(
            "There is no data after clean, the data becomes empty after being cleaned in the latest period"
        )
        return ""

    # if the_end_date_put_in != t1:
    #     print(the_end_date_put_in)
    #     print(t1)
    #     print("*********The final time is not t-1, not calculated")
    #     return ""
    # else:
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
    ruletype = rule.split("_")[0]  # example： R00001_xxxxx
    eval(ruletype)(ruleid, df, table, column, param, index, url, f)


def R00001(ruleid, df, table, column, param, index, url, f):
    """
    R00001_{L}-order difference value does not exceed {N} daily moving window {M} upper and lower standard deviations
    """
    s_param = param.split(" ")
    # Parameters are extracted in order, and when configured in the configuration file, they are also in order.
    diff_deep = int(s_param[0])
    # Moving window length
    window_value = int(s_param[1])
    # How many times the standard deviation is considered an outlier
    std_times = float(s_param[2])
    # Field name of upper standard deviation
    std_top = "diff_" + str(std_times) + "times_mstd" + str(window_value)
    # The field name of the lower standard deviation
    std_bottom = "diff_-" + str(std_times) + "times_mstd" + str(window_value)

    if len(index) > 1:
        dim_str = str(index[0:-1])  # Except the last one as the dimension
        time_str = str(index[-1])  # The last one is the time x axis
        dimention = df.groupby(index[0:-1]).count().index  # Combination of dimensions
    else:
        dim_str = "_"  # In order to run on win, special characters such as asterisk or less than greater than sign cannot be used
        time_str = str(index[0])
        dimention = ["_"]  # There is no other dimension except time

    for groupset in dimention:
        print(
            "R00001"
            + ruleid
            + "------------Processing group---"
            + table
            # + filename
            + str(index)
            + "--------"
            + str(groupset)
            + "---------------Processing group----------------"
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

        if obj.size <= 7:
            print("Time series is less than 7. exit")
            continue

        # Difference The difference between the previous time and the previous time. The need_diff parameter controls whether the difference is needed, and the diff_deep parameter controls the order of the diff
        obj["diff"] = obj[
            column
        ]  # Increase the diff field equal to the original value when initialized
        i = diff_deep  # diff_deep order difference
        while i > 0:
            obj["diff"] = obj["diff"].diff()
            i = i - 1

        # Moving average Moving average window_value day average
        obj["diff_ma" + str(window_value)] = (
            obj["diff"].rolling(window=window_value, center=False).mean()
        )
        # Moving std moving standard deviation std_times times standard deviation
        obj[std_top] = (
            std_times * obj["diff"].rolling(window=window_value, center=False).std()
        )
        obj[std_bottom] = (
            -std_times * obj["diff"].rolling(window=window_value, center=False).std()
        )

        # Determine whether the indicator is within the range Increase the upward or downward fluctuation
        conditions = [
            (obj["diff"] > obj[std_top]) | (obj["diff"] < obj[std_bottom]),
            1 == 1,
        ]
        conditios_up = [(obj["diff"] > obj[std_top]), 1 == 1]
        conditios_down = [(obj["diff"] < obj[std_bottom]), 1 == 1]
        choices = [True, False]  # True means an alert is triggered
        obj["res"] = np.select(conditions, choices, default=False)
        obj["up"] = np.select(conditios_up, choices, default=False)
        obj["down"] = np.select(conditios_down, choices, default=False)

        if (
            obj.loc[obj.index[-1]]["res"] == False
        ):  # The last point must be an early warning point, otherwise no warning is output
            print(
                "The last point must be an early warning point, otherwise no warning is output"
            )
            continue

        # Only record the last warning point
        last_dt = obj[obj["res"] == True].index[-1]
        vv = obj.loc[last_dt][column]  # Trigger warning value
        sBD = "Upward Fluctuation"
        if obj.loc[last_dt]["up"] == True:
            sBD = "Upward Fluctuation"
        elif obj.loc[last_dt]["up"] == False:
            sBD = "Downward Fluctuate"

        alerttext = (
            Tools.special_char_remove(dim_str)
            + ","
            + Tools.special_char_remove(str(groupset))
            + ","
            + table
            + ",["
            + column
            + "],"
            + sBD
            + " Abnormal,"
            + param
        )
        data_file = os.path.join("..", table + ".xlsx")

        f.write(
            str(uuid.uuid1())
            + ","
            + ruleid
            + ",R00001,[Volatility warning],"
            + Tools.time_dim_to_str(last_dt)
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
    R00005_Absolute value{>=<}{T}
    """
    # fill None value to Zero
    df.fillna(0, inplace=True)
    # params example: "< 100"
    # so we split it with whitespace then we got the operation and threshold value
    params = param.split(" ")
    oper = params[0]  # >=<
    value = float(params[1])  # Threshold

    # If the length of index is one, it means only the time dimension, if it is greater than 1, take the dimension index[0:-1] other than the last time dimension as groupby
    if len(index) > 1:
        dim_str = str(index[0:-1])  # Other dimensions
        time_str = str(index[-1])  # Time dimension
        temp = (
            df.groupby(index[0:-1]).count().index
        )  # List of other dimensions, group processing
    else:
        time_str = str(index[0])
        dim_str = "_"
        temp = ["_"]  # There is no other dimension except time

    for groupset in temp:
        print(
            "R00005"
            + "--------ruleid:"
            + ruleid
            + "------------Processing group---"
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

        if type(dt_end) == str and dt_end == "":
            continue

        obj = dd[:dt_end][[column]]

        obj["thresholdvalue"] = value
        obj["-thresholdvalue"] = -1 * value
        if oper == ">":
            conditions = [abs(obj[column]) > obj["thresholdvalue"], 1 == 1]
            print("conditions: ", conditions)
            print("thresholdvalue", obj["thresholdvalue"])
            oper_str = " greater than "
        elif oper == "<":
            conditions = [abs(obj[column]) < obj["thresholdvalue"], 1 == 1]
            oper_str = " less than "
        elif oper == "=":
            conditions = [abs(obj[column]) == obj["thresholdvalue"], 1 == 1]
            oper_str = " is equal to "

        choices = [True, False]
        obj["res"] = np.select(conditions, choices, default=False)

        alerttext = (
            Tools.special_char_remove(dim_str)
            + ","
            + Tools.special_char_remove(str(groupset))
            + ","
            + table
            + ",["
            + column
            + "],Absolute value"
            + oper_str
            + "Threshold,"
            + str(value)
        )

        # The last point must be an early warning point, otherwise no warning will be output and cannot be used is must == there will be bugs
        if obj.loc[obj.index[-1]]["res"] == False:
            continue

        last_dt = obj[obj["res"] == True].index[-1]
        vv = obj.loc[last_dt][column]
        data_file = os.path.join("..", table + ".xlsx")
        f.write(
            str(uuid.uuid1())
            + ","
            + ruleid
            + ",R00005,[High limit warning],"
            + Tools.time_dim_to_str(last_dt)
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
    R00003 multi-condition rule matching,
    """

    column_lists = column.split(" ")
    param_lists = param.split(" ")
    l = len(column_lists)
    oper_lists = param_lists[:l]
    value_lists = param_lists[l:]
    value_lists = [Tools.maybe_float(v) for v in value_lists]

    if len(column_lists) == len(oper_lists) == len(value_lists):
        pass
    else:
        print(
            "Please enter the matching field parameters and values, separated by a space, this rule will not be executed："
            + ruleid
        )
        return 0

    if (
        len(index) > 1
    ):  # If the length of index is one, it means there is only time dimension. If it is greater than 1, take the dimension idx[0:-1] other than the last time dimension as groupby
        dim_str = str(index[0:-1])  # Other dimensions
        time_str = str(index[-1])  # Time dimension
        dimention = (
            df.groupby(index[0:-1]).count().index
        )  # List of other dimensions, group processing
    else:
        time_str = str(index[0])
        dim_str = "_"
        dimention = ["_"]  # There is no other dimension except time

    for groupset in dimention:
        print(
            "R00003--------ruleid:"
            + ruleid
            + "------------Processing group----"
            + table
            + str(index)
            + "-------"
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

        if type(dt_end) == str and dt_end == "":
            continue

        obj = dd[:dt_end][list(set(column_lists))]
        c_markers_lists = []
        for c, v, o in zip(column_lists, value_lists, oper_lists):
            keyname = (
                c + o + str(v)
            )  # The field operator and the value form a unique keyname to form a new column
            # print(keyname)
            obj[keyname + "_thresholdvalue"] = v
            obj[keyname + "markers"] = Tools.get_truth(
                obj[c], o, obj[keyname + "_thresholdvalue"]
            )
            c_markers_lists.append(keyname + "markers")

        obj["res"] = obj[c_markers_lists].all(
            axis=1
        )  # All conditions must be met to trigger an alert

        alerttext = (
            Tools.special_char_remove(dim_str)
            + ","
            + Tools.special_char_remove(str(groupset))
            + ","
            + table
            + ","
            + Tools.special_char_remove(str(column_lists))
            + ","
            + Tools.special_char_remove(str(oper_lists))
            + ","
            + Tools.special_char_remove(str(value_lists))
        )

        if (
            obj.loc[obj.index[-1]]["res"] == False
        ):  # The last point must be an early warning point, otherwise no warning is output
            continue

        last_dt = obj[obj["res"] == True].index[-1]
        vv = list(obj.loc[last_dt][column_lists])
        f.write(
            str(uuid.uuid1())
            + ","
            + ruleid
            + ",R00003,[Multi-condition warning],"
            + Tools.time_dim_to_str(last_dt)
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

        f_last_alerts = open(csv_file_name, "w", encoding="utf-8")
        f_last_alerts.write(
            "alarmid,ruleid,trigger_rule,rule_type,date,date_type,dimension_name,dimension_value,table,field,description,parameter,value,graph,data,url"
            + "\n"
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

        return pd.read_csv(csv_file_name, encoding="utf-8")


def add(name, df):
    """
    add df to global panel_data 
    name: path.filename
    df: input pandas Dataframe
    """
    panel_data[name] = df

