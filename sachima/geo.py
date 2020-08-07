import os
import requests
import json
import time

from sachima.log import logger
from sachima import conf

from io import BytesIO

BAIDU_GEO_TOKEN = conf.get("BAIDU_GEO_TOKEN")
QQ_GEO_TOKEN = conf.get("QQ_GEO_TOKEN")
AMAP_GEO_TOKEN = conf.get("AMAP_GEO_TOKEN")


def poi_compound_dict(
    dim={"K001": "subway", "K002": "hospital", "K003": "school"},
    dis=[500, 1000],
    lat=31.191869,
    lng=121.446756,
    onlycnt=False,
    onlyfarest=True,
    savetofile=False,
):
    """
    DIM = {
        "K001": "subway",
        "K002": "hospital",
        "K003": "school"
    }

    DIS = [500, 1000, 1500, 2000]

    lat = 31.191869 
    lng = 121.446756
    """
    res = {}
    for k in dim:
        for d in dis:
            key = k + "_" + str(d)  # eg. K001_1000
            key_cnt = key + "_CNT"  # eg. K001_1000_CNT
            poi_json = poi(lat, lng, dim.get(k), radius=d)
            if onlycnt is False:
                if onlyfarest is False:
                    res[key] = str(poi_json)
                elif d == max(dis):
                    res[key] = str(poi_json)
            res[key_cnt] = poi_json.get("count")

    return res


def poi(lat, lng, keywords, radius=1000):
    """
    Get poi information from amap \n
    https://lbs.amap.com/api/webservice/guide/api/search \n
    """
    logger.info((lat, lng, keywords, radius))
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
        logger.debug(r)
        if r.get("info") == 'USER_DAILY_QUERY_OVER_LIMIT':
            raise 'USER_DAILY_QUERY_OVER_LIMIT'
        return r
    except Exception as e:
        raise e


def panorama(lat, lng):
    """
    Panorama information query
    return Image Buffer
    you can open the buffer use PIL.Image.open(buffer)
    """
    if BAIDU_GEO_TOKEN is None:
        logger.info("error: Must config BAIDU_GEO_TOKEN in sachima_config.py")
        raise "Must config BAIDU_GEO_TOKEN in sachima_config.py"

    url = "http://api.map.baidu.com/panorama/v2"
    values = {"ak": BAIDU_GEO_TOKEN, "fov": 180, "location": "{},{}".format(lng, lat)}
    try:
        logger.info("Fetching {},{} panorama picture ...".format(lat, lng))
        r = requests.get(url, values).content
        b = BytesIO()
        b.write(r)
        return b
    except Exception as e:
        raise e


def fetchBaiduLatLng(address):
    """
    Use baidu map api to get the latitude and longitude of city from the Internet. \n
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
        logger.info(r)
        if r.get("status") != 0:
            return {}
        else:
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
        logger.info("fetchBaiduGeo for %s error: %s" % (address, e))
        raise e


def fetchQQLatLng(address):
    """
    Use qq map api to get latitude and longitude from the Internet.
    https://lbs.qq.com/miniProgram/jsSdk/jsSdkGuide/methodGeocoder
    """
    if QQ_GEO_TOKEN is None:
        logger.info("error: Must config QQ_GEO_TOKEN in sachima_config.py")
        raise "Must config QQ_GEO_TOKEN in sachima_config.py"

    values = {"key": QQ_GEO_TOKEN, "output": "json", "address": address}

    url = "https://apis.map.qq.com/ws/geocoder/v1/"
    try:
        r = requests.get(url, params=values).json()
        if r.get("status") == 347:
            return {}
        else:
            return {
                "qq_lat": r.get("result").get("location").get("lat"),
                "qq_lng": r.get("result").get("location").get("lng"),
                "qq_title": r.get("result").get("title"),
                "qq_adcode": r.get("result").get("ad_info").get("adcode"),
                "qq_province": r.get("result")
                .get("address_components")
                .get("province"),
                "qq_city": r.get("result").get("address_components").get("city"),
                "qq_district": r.get("result")
                .get("address_components")
                .get("district"),
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
        logger.info("fetchQQGeo for %s error: %s！" % (address, e))
        raise e


def fetchAmapLatLng(address):
    """
    Use amap api to get latitude and longitude from the Internet.
    https://lbs.qq.com/miniProgram/jsSdk/jsSdkGuide/methodGeocoder
    """
    logger.info("fetching {} amap geo info".format(address))
    if AMAP_GEO_TOKEN is None:
        logger.info("error: Must config AMAP_GEO_TOKEN in sachima_config.py")
        raise "Must config AMAP_GEO_TOKEN in sachima_config.py"
    par = {"address": address, "key": AMAP_GEO_TOKEN}
    base = "http://restapi.amap.com/v3/geocode/geo"
    r = requests.get(base, par).json()
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
        "amap_street": str(geocodes.get("street")),
        "amap_number": str(geocodes.get("number")),
        "amap_level": geocodes.get("level"),
    }
