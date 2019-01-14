import datetime as dt
import pandas as pd
import numpy as np
import sachima.mail as mailer
import os
import re
from sachima.htmlstyle import apply_html_style


def run(data_in):
    df1 = data_in[0]
    df1 = df1.describe()
    df1table = df1.to_html(border=0, index=True)
    tablelists = [df1table]
    content = apply_html_style(
        tablelists, title="EMAIL正文格式化例子", cssfile="tohtmlstyle_black.css"
    )

    tolist = [""]
    cclist = []

    mailer.send_mail(tolist, cclist, "邮件正文html格式化例子_2", content, [], ishtml=True)

    return df1
