import datetime as dt
import pandas as pd
import numpy as np
import sachima.mail as mailer
import os
import re
from sachima.htmlstyle import apply_html_style


def run(data_in, params):
    df1 = data_in[0]
    # df1 = df1.describe()
    # df1.reset_index(level=0, inplace=True)
    df1["anotherhandler加的列"] = 1
    return df1[: params["yourlines"]]  # 通过参数来过滤行数 。
