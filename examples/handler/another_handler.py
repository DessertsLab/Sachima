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
    col_sssh = params.get("所属商户", None)
    if col_sssh:
        df1 = df1[df1["所属商户"] == col_sssh]

    return df1[: params["行数"]]  # 通过参数来过滤行数 。
