"""
title: s_sachima_funnel_example
"""
from sachima.main_runner import run
from sachima.filter_enum import FilterEnum as _
from sachima.params import Filter
from sachima.wrappers import send, timer

from services.db_connects import db
import datetime as dt

db = db()

@timer
def main(api_params={}):
    PARAM_IN = {
        "model": [("example_data/funnel2.csv", "csv")],
        "handler": ["s_sachima_funnel_example"],
        "params": {
        },
        "filters": [],
        "vis": {"type": "funnel", "title": "漏斗分析1.0"},
    }

    return run(PARAM_IN, api_params)


if __name__ == "__main__":
    main()

