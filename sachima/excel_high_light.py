# -*- coding: utf-8 -*-
import pandas as pd
import sachima.Color as co
from sachima.tools import Tools
from PIL import ImageFont  # Pillow
import random


class ExcelHighLighter:
    def __init__(
        self,
        filename,
        highcols=["触发规则", "规则类型"],
        hide=["A", "B", "N", "O"],
        colfilter=True,
    ):
        self.filename = filename
        self.srcdf = pd.read_csv(filename, encoding="GBK")
        self.hide = hide
        self.colfilter = colfilter
        self.highcols = highcols

    def to_excel(self, tofile=None):
        FONT = ImageFont.truetype("msyh.ttc", size=16)
        hidden_cols = self.hide
        cols_need_diff_color = self.highcols
        COLOR_NUMBERS = 100

        # pd.io.formats.excel.header_style = None
        # pd.formats.header_style = None
        pd.io.formats.style = None

        if tofile is None:
            tofile = self.filename.replace("csv", "xlsx")
        df = self.srcdf
        writer = pd.ExcelWriter(tofile)
        df.to_excel(
            writer,
            "alerts",
            encoding="utf_8_sig",
            index=False,
            startrow=1,
            header=False,
        )
        workbook = writer.book
        worksheet_alerts = writer.sheets["alerts"]

        rows = df.shape[0]
        cols = df.shape[1]
        max_col_string = Tools.excel_colnum_string(cols)

        head_cell_format = workbook.add_format(
            {
                "font_color": "black",
                "bg_color": "#e6e6e6",
                "bold": True,
                "align": "center",
            }
        )

        for col_num, value in enumerate(df.columns.values):
            worksheet_alerts.write(0, col_num, value, head_cell_format)

        # gen_hex_colors(100)

        formats = []
        for color in co.gen_hex_colors("#01a5af", COLOR_NUMBERS):
            formats.append(
                workbook.add_format(
                    {"bg_color": color, "font_color": "#352c0a"}
                )
            )

        worksheet_alerts.freeze_panes(1, 0)
        worksheet_alerts.autofilter("A1:" + max_col_string + "1")

        # (width,h) = FONT.getsize('test text')

        # 根据字符的长度设置列宽，如果没有数据不设置
        def get_col_widths(dataframe):
            # First we find the maximum length of the index column
            idx_max = max(
                [len(str(s)) for s in dataframe.index.values]
                + [len(str(dataframe.index.name))]
            )
            # Then, we concatenate this to the max of the lengths of column
            #  name and its values for each column, left to right
            return [idx_max] + [
                max(
                    [FONT.getsize(str(s))[0] for s in dataframe[col].values]
                    + [FONT.getsize(col)[0]]
                )
                for col in dataframe.columns
            ]

        # 宽度
        if rows > 0:  # 必须有记录 不然的话会把列宽设置为0
            for i, width in enumerate(get_col_widths(df)):
                worksheet_alerts.set_column(
                    i, i - 1, width * 0.13953488372093023
                )

        # 隐藏
        for hi in hidden_cols:
            worksheet_alerts.set_column(
                hi + ":" + hi, None, None, {"hidden": 1}
            )

        # 颜色
        s_combine_color_diff_cols = ""
        for sname in cols_need_diff_color:
            s_combine_color_diff_cols += df[sname].astype(str)

        # for i in df['idx'].drop_duplicates()
        # int(random.uniform(0,COLOR_NUMBERS-1))

        df["idx"] = pd.Categorical(s_combine_color_diff_cols).codes
        # random_color_index = int(random.uniform(0,100))
        for i in range(2, rows + 2):
            random.seed(df.iloc[i - 2].idx)
            worksheet_alerts.conditional_format(
                "A" + str(i) + ":" + max_col_string + str(i),
                {
                    "type": "text",
                    "criteria": "not containing",
                    "value": "white",
                    "format": formats[int(random.uniform(0, 100))],
                },
            )
        writer.save()


# if __name__ == "__main__":
#     filename = "/Users/zhangmk/Desktop/alertlist20180604.csv"
#     ehl = ExcelHighLighter(
#         filename,
#         highcols=["触发规则", "规则类型", "日期类型", "维度名称", "表格", "字段"],
#         hide=["A", "B", "N", "O"],
#         colfilter=True,
#     )
#     ehl.to_excel()
