# -*- coding: utf-8 -*-
"""
@author: mk
"""


def app_style_to_excel(dfname,
                       sheetname,
                       range='A1:R',
                       autofilter=0,
                       style='Table Style Light 9'):
    columns = [{'header': c} for c in dfname.columns]
    options = {
        'style': 'Table Style Light 9',
        'header_row': True,
        'banded_columns': False,
        'autofilter': 0,
        'columns': columns
    }
    # Add a table to the worksheet.
    sheetname.add_table(range + str(len(dfname) + 1), options)
