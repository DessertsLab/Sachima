"""
title: s_scatter3d
author: mk
"""
from sachima.main_runner import run
from sachima.filter_enum import FilterEnum as _
from sachima.params import Filter
from sachima.wrappers import send, timer

from services.db_connects import db as database

db = database()


@timer
# @send
def main(api_params={}):
    PARAM_IN = {
        "params": {},
        "filters": [],
        "model": [("example_data/life_expectancy.json", "json")],
        "handler": ["s_scatter3d"],
        "vis": {
            "type": "scatter3d",
            "title": "Life expectancy 3d scatter graph",
            "params": {
                "upleft": ["Income", "Life Expectancy"],
                "downleft": ["Income", "Population"],
                "upright": ["Country", "Income"],
                "downright": ["Life Expectancy", "Population"],
            },
        },
    }

    return run(PARAM_IN, api_params)


if __name__ == "__main__":
    res = main()
