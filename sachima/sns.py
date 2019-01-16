from urllib import request
from urllib import parse
import json
import pandas as pd


def send_request(host, path, webhook, querys, data):
    try:
        url = host + path + "?" + querys
        headers = {"Content-Type": "application/json"}
        req = request.Request(
            url=url, headers=headers, data=json.dumps(data).encode("utf-8")
        )
        response = request.urlopen(req)
        content = response.read().decode("utf-8")
    except:
        raise
    return content


def send_dingding(title, data, webhook):
    host = "https://oapi.dingtalk.com/"
    path = "robot/send"
    querys = "access_token=" + webhook

    jsondata = {
        "msgtype": "markdown",
        "markdown": {"title": title, "text": data},
    }
    return send_request(host, path, webhook, querys, jsondata)
