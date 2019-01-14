import datetime as dt
import pandas as pd
import numpy as np
import sachima.mail as mailer
import os
import re
from sachima.htmlstyle import apply_html_style
from sachima.params import Filter


def run(data_in):
    df1 = data_in[0]
    # df1 = pd.DataFrame({
    #         '0': 1.,
    #         'riqi': pd.date_range('2018-01-01', '2018-01-04'),
    #         '字段A': '20181228',
    #         '字段B': '这是一段测试文字测试字段的长度是否能自动调整',
    #         '字段C': pd.Series(1, index=list(range(4)), dtype='float32'),
    #         '字段D': np.array([3] * 4, dtype='int32'),
    #         '字段E': pd.Categorical(["test", "train", "test", "train"]),
    #         '字段F': '这是一段测试文字测试字段的长度是否能自动调整',
    #         '字段G': '这是一段测试文字测试字段的长度是否能自动调整这是一段测试' +
    #         '文字测试字段的长度是否能自动调整这是一段测试文字测试字段的长度是否能自动调整'
    #     })

    print("$" * 40)
    print(type(df1))
    # df1 = pd.concat([df1,df1,df1])
    return df1
