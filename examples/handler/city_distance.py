import datetime as dt
import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt
import json
import os
import re
import itertools


def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return round(c * r * 1000, 2)


def run(data_in, params):
    areas = ""
    with open("data/areas.json", encoding="utf-8") as f:
        areas = f.read()

    areas_dict = json.loads(areas)

    city_dict = {}

    for city in (
        areas_dict["result"][1]
        + areas_dict["result"][0]
        + areas_dict["result"][2]
    ):
        if "市" in city["fullname"]:
            city_dict[city["fullname"]] = [
                city["location"]["lng"],
                city["location"]["lat"],
            ]

    res = []
    for c in itertools.combinations(city_dict.keys(), 2):
        from_city_lng = city_dict[c[0]][0]
        from_city_lat = city_dict[c[0]][1]
        to_city_lng = city_dict[c[1]][0]
        to_city_lat = city_dict[c[1]][1]
        dist = haversine(from_city_lng, from_city_lat, to_city_lng, to_city_lat)
        res.append(
            (
                c[0],
                from_city_lng,
                from_city_lat,
                c[1],
                to_city_lng,
                to_city_lat,
                dist,
            )
        )

    df1 = pd.DataFrame(
        res,
        columns=[
            "出发城市",
            "出发城市经度",
            "出发城市维度",
            "终点城市",
            "终点城市经度",
            "终点城市维度",
            "距离（米）",
        ],
    )

    col_from = params.get("出发城市", None)
    col_to = params.get("终点城市", None)
    if col_from:
        df1 = df1[df1["出发城市"].isin(col_from)]
    if col_to:
        df1 = df1[df1["终点城市"].isin(col_to)]

    return df1[: int(params["行数"])]
    # return df1


# if __name__ == "__main__":
#     d = run([], [])
#     d.to_csv("data/city_dis.csv")

