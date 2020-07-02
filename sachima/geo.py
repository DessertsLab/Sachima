# -*- coding: utf8 -*-
import os
import requests
import json
import time

from sachima.log import logger
from sachima import conf

from PIL import Image
from io import BytesIO

BAIDU_GEO_TOKEN = conf.get("BAIDU_GEO_TOKEN")
QQ_GEO_TOKEN = conf.get("QQ_GEO_TOKEN")
AMAP_GEO_TOKEN = conf.get("AMAP_GEO_TOKEN")


# poi
def poi(lat, lng, keywords, radius=1000):
    """
    高德地图获取poi信息 \n
    https://lbs.amap.com/api/webservice/guide/api/search \n
    """
    logger.info((lat, lng))
    if AMAP_GEO_TOKEN is None:
        logger.info("error: Must config AMAP_GEO_TOKEN in sachima_config.py")
        raise "Must config AMAP_GEO_TOKEN in sachima_config.py"

    url = "https://restapi.amap.com/v3/place/around"
    values = {
        "key": AMAP_GEO_TOKEN,
        "location": "{},{}".format(lng, lat),
        "keywords": keywords,
        "types": "",
        "radius": radius,  # default one mile
    }
    try:
        r = requests.get(url, values).json()
        logger.info(r)
        return r
    except Exception as e:
        raise e


def panorama(lat, lng):
    """
    全景信息查询
    """
    if BAIDU_GEO_TOKEN is None:
        logger.info("error: Must config BAIDU_GEO_TOKEN in sachima_config.py")
        raise "Must config BAIDU_GEO_TOKEN in sachima_config.py"

    url = "http://api.map.baidu.com/panorama/v2"
    values = {"ak": BAIDU_GEO_TOKEN, "fov": 180, "location": "{},{}".format(lng, lat)}
    try:
        logger.info("正在获取{},{}全景图片。。。".format(lat, lng))
        r = requests.get(url, values).content
        b = BytesIO()
        b.write(r)
        return Image.open(b)
        # logger.info(r)
    except Exception as e:
        raise e


def fetchBaiduLatLng(address):
    """
    利用baidu map api从网上获取city的经纬度。\n
    http://lbsyun.baidu.com/index.php?title=webapi \n
    """
    if BAIDU_GEO_TOKEN is None:
        logger.info("error: Must config BAIDU_GEO_TOKEN in sachima_config.py")
        raise "Must config BAIDU_GEO_TOKEN in sachima_config.py"
    values = {
        "address": address,
        "ret_coordtype": "",
        "ak": BAIDU_GEO_TOKEN,
        "sn": "",
        "precise": 1,
        "output": "json",
        "callback": "",
    }
    url = "http://api.map.baidu.com/geocoder/v2/"
    try:
        r = requests.get(url, params=values).json()
        return {
            "baidu_lat": r.get("result").get("location").get("lat"),
            "baidu_lng": r.get("result").get("location").get("lng"),
            "baidu_precise": r.get("result").get("precise"),
            "baidu_confidence": r.get("result").get("confidence"),
            "baidu_comprehension": r.get("result").get("comprehension"),
            "baidu_level": r.get("result").get("level"),
            "baidu_status": r.get("status"),
        }
    except Exception as e:
        logger.info("fetchBaiduGeo for %s error: %s 发生异常！" % (address, e))
        raise e


def fetchQQLatLng(address):
    """
    利用qq map api从网上获取city的经纬度。
    https://lbs.qq.com/miniProgram/jsSdk/jsSdkGuide/methodGeocoder
    """
    if QQ_GEO_TOKEN is None:
        logger.info("error: Must config QQ_GEO_TOKEN in sachima_config.py")
        raise "Must config QQ_GEO_TOKEN in sachima_config.py"

    values = {"key": QQ_GEO_TOKEN, "output": "json", "address": address}

    url = "https://apis.map.qq.com/ws/geocoder/v1/"
    try:
        r = requests.get(url, params=values).json()
        return {
            "qq_lat": r.get("result").get("location").get("lat"),
            "qq_lng": r.get("result").get("location").get("lng"),
            "qq_title": r.get("result").get("title"),
            "qq_adcode": r.get("result").get("ad_info").get("adcode"),
            "qq_province": r.get("result").get("address_components").get("province"),
            "qq_city": r.get("result").get("address_components").get("city"),
            "qq_district": r.get("result").get("address_components").get("district"),
            "qq_street": r.get("result").get("address_components").get("street"),
            "qq_street_number": r.get("result")
            .get("address_components")
            .get("street_number"),
            "qq_similarity": r.get("result").get("similarity"),
            "qq_deviation": r.get("result").get("deviation"),
            "qq_reliability": r.get("result").get("reliability"),
            "qq_level": r.get("result").get("level"),
            "qq_status": r.get("status"),
            "qq_message": r.get("message"),
        }
    except Exception as e:
        logger.info("fetchQQGeo for %s error: %s 发生异常！" % (address, e))
        raise e


def fetchAmapLatLng(address):
    """
    使用高德API
    """
    if AMAP_GEO_TOKEN is None:
        logger.info("error: Must config AMAP_GEO_TOKEN in sachima_config.py")
        raise "Must config AMAP_GEO_TOKEN in sachima_config.py"
    par = {"address": address, "key": AMAP_GEO_TOKEN}
    base = "http://restapi.amap.com/v3/geocode/geo"
    r = requests.get(base, par).json()
    # logger.info(r)
    geocodes = {}
    GPS = [None, None]
    if r.get("count") != "0":
        geocodes = r.get("geocodes")[0]
        GPS = geocodes.get("location").split(",")
    return {
        "amap_lat": GPS[1],
        "amap_lng": GPS[0],
        "amap_status": r.get("status"),
        "amap_info": r.get("info"),
        "amap_infocode": r.get("infocode"),
        "amap_count": r.get("count"),
        "amap_formatted_address": geocodes.get("formatted_address"),
        "amap_country": geocodes.get("country"),
        "amap_province": geocodes.get("province"),
        "amap_citycode": geocodes.get("citycode"),
        "amap_city": geocodes.get("city"),
        "amap_adcode": geocodes.get("adcode"),
        "amap_street": geocodes.get("street"),
        "amap_number": geocodes.get("number"),
        "amap_level": geocodes.get("level"),
    }


def district(self):
    self.url = "https://apis.map.qq.com/ws/district/v1/list"
    try:
        r = requests.get(self.url, params=self.values).json()
        return r
    except:
        print("获取行政区划发生异常！")


class ISO3166(object):
    def __init__(self):
        self.china = {
            "安徽省": "CN-34",  # Anhui
            "北京市": "CN-11",  # Beijing
            "重庆市": "CN-50",  # Chongqing
            "福建省": "CN-35",  # Fujian
            "甘肃省": "CN-62",  # Gansu
            "广东省": "CN-44",  # Guangdong
            "广西壮族自治区": "CN-45",  # Guangxi
            "贵州省": "CN-52",  # Guizhou
            "海南省": "CN-46",  # Hainan
            "河北省": "CN-13",  # Hebei
            "黑龙江省": "CN-23",  # Heilongjiang
            "河南省": "CN-41",  # Henan
            "湖北省": "CN-42",  # Hubei
            "湖南省": "CN-43",  # Hunan
            "江苏省": "CN-32",  # Jiangsu
            "江西省": "CN-36",  # Jiangxi
            "吉林省": "CN-22",  # Jilin
            "辽宁省": "CN-21",  # Liaoning
            "内蒙古自治区": "CN-15",  # Nei Mongol
            "宁夏回族自治区": "CN-64",  # Ningxia Hui
            "青海省": "CN-63",  # Qinghai
            "陕西省": "CN-61",  # Shaanxi
            "山东省": "CN-37",  # Shandong
            "上海市": "CN-31",  # Shanghai
            "山西省": "CN-14",  # Shanxi
            "四川省": "CN-51",  # Sichuan
            "天津市": "CN-12",  # Tianjin
            "新疆维吾尔自治区": "CN-65",  # Xinjiang Uygur
            "西藏自治区": "CN-54",  # Xizang
            "云南省": "CN-53",  # Yunnan
            "浙江省": "CN-33",  # Zhejiang
            "台湾省": "CN-71",  # Taiwan
            "香港特别行政区": "CN-91",  # Hong Kong
            "澳门特别行政区": "CN-92",  # Macao
        }


# class qqgeoAsync(object):
#     loop = asyncio.get_event_loop()
#     async def async_get_geo(self,name):
#         url = 'https://apis.map.qq.com/ws/geocoder/v1/'
#         params = {
#             'address': name,
#             'key': '',
#             'output': 'json',
#         }
#         async with aiohttp.ClientSession(loop=loop) as session:
#             async with session.get(url, params=params) as response:
#                 response = await response.json()
#                 if response['status']!=347 and response['status']!=120:
#                     print(response)
#                     return response['result']['location']['lat'], response['result']['location']['lng']
#                 else:
#                     return 0,0
