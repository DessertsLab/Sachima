# -*- coding: utf8 -*-
import os
import requests
import json
import time

from sachima.log import logger
from sachima import conf

BAIDU_GEO_TOKEN = conf.get("BAIDU_GEO_TOKEN")
QQ_GEO_TOKEN = conf.get("QQ_GEO_TOKEN")


def fetchBaiduLatLng(address):
    """
    利用baidu map api从网上获取city的经纬度。\n
    http://lbsyun.baidu.com/index.php?title=webapi \n
    return lat, lng, precise, confidence, comprehension, level
    """
    if BAIDU_GEO_TOKEN is None:
        logger.info("error: Must config BAIDU_GEO_TOKEN in sachima_config.py")
        raise "Must config BAIDU_GEO_TOKEN in sachima_config.py"
    values = {
        "address": "",
        "ret_coordtype": "",
        "ak": BAIDU_GEO_TOKEN,
        "sn": "",
        "precise": 1,
        "output": "json",
        "callback": "",
    }
    url = "http://api.map.baidu.com/geocoder/v2/"
    values["address"] = address
    try:
        r = requests.get(url, params=values).json()
        lat, lng, precise, confidence, comprehension, level, status = (
            r.get("result").get("location").get("lat"),
            r.get("result").get("location").get("lng"),
            r.get("result").get("precise"),
            r.get("result").get("confidence"),
            r.get("result").get("comprehension"),
            r.get("result").get("level"),
            r.get("status"),
        )
        return lat, lng, precise, confidence, comprehension, level, status
    except Exception as e:
        logger.info("fetchBaiduGeo for %s error: %s 发生异常！" % (address, e))
        raise e


def fetchQQLatLng(address):
    """
    利用qq map api从网上获取city的经纬度。
    https://lbs.qq.com/miniProgram/jsSdk/jsSdkGuide/methodGeocoder
    """
    values = {"key": QQ_GEO_TOKEN, "output": "json", "address": address}

    url = "https://apis.map.qq.com/ws/geocoder/v1/"
    try:
        r = requests.get(url, params=values).json()
        print(r)
        time.sleep(0.2)
        lat, lng = (
            r.get("result").get("location").get("lat"),
            r.get("result").get("location").get("lng"),
        )
        return lat, lng
    except Exception as e:
        logger.info("fetchQQGeo for %s error: %s 发生异常！" % (address, e))
        raise e

    # def geocoder(self, address, region='', ret_coordtype='', callback=''):
    #     self.url = 'https://apis.map.qq.com/ws/geocoder/v1/'
    #     self.values['address'] = address
    #     self.values['region'] = region
    #     self.values['ret_coordtype'] = ret_coordtype
    #     self.values['callback'] = callback
    #     try:
    #         r = requests.get(self.url, params=self.values).json()
    #         self.lat, self.lng = r['result']['location']['lat'], r['result']['location']['lng']
    #         return self.lat, self.lng
    #     except:
    #         print('城市: %s 发生异常！' % (address,))


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

if __name__ == "__main__":
    print(fetchBaiduGeo("中山市东区中山三路1号之二"))
    # geo = GeoQQ()
    # # geo = GeoBaidu()
    # # geo = GeoBaidu()、
    # for i in range(1):
    #     cityName = "安徽省阜阳市"
    #     longitude, latitude = geo.geocoder(cityName)
    #     print("%s \n经度：%f\n纬度：%f\n" % (cityName, longitude, latitude))
    # # print(geo.district())

    # # 异步调用例子
    # users = 'asset/users.csv'
    # df_users = pd.read_csv(users,encoding='utf-8',sep='>')
    # df_users['address'] = df_users['current_address'].fillna(df_users['company_address'])
    # # df_users[['longitude','latitude']] = df_users['address'].apply(lambda x: get_geo(x)).apply(pd.Series)
    # # df_users['current_address'] = ''
    # # df_users['company_address'] = ''
    # tasks = [async_get_geo(addr) for addr in  df_users['address'][:5]]
    # a = loop.run_until_complete(asyncio.gather(*tasks))
    # print(a)
    # # df_users.to_csv('asset/users_withgeo.csv')
    # # get_geo('莆田市福建省莆田市荔城区镇海街道八二一南街185号')
    # exit()


# #使用高德API
# def geocodeG(address):
#     par = {'address': address, 'key': ''}
#     base = 'http://restapi.amap.com/v3/geocode/geo'
#     response = requests.get(base, par)
#     answer = response.json()
#     GPS=answer['geocodes'][0]['location'].split(",")
#     return GPS[0],GPS[1]

# #使用百度API
# def geocodeB(address):
#     base = url = "http://api.map.baidu.com/geocoder?address=" + address + "&output=json&key="
#     response = requests.get(base)
#     answer = response.json()
#     return answer['result']['location']['lng'],answer['result']['location']['lat']

