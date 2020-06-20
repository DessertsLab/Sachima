import json as js
import os
import re

from sachima.log import logger


def drill(json_dict, path_desc):
    if not isinstance(json_dict, dict):
        raise TypeError("wrong type for first param should be dict")
    for element in path_desc:
        logger.debug("handle element：" + str(element))
        if len(json_dict) == 0:
            return ""
        # logger.debug(json_dict)
        if isinstance(element, str):
            # logger.debug("type(json_dict): " + str(type(json_dict)))
            if isinstance(json_dict, str):
                m = re.search(element, json_dict)
                if m is None:
                    return ""
                else:
                    return m.group()
            else:
                json_dict = json_dict.get(element, {})
                logger.debug("json_dict update: " + str(json_dict))
        elif isinstance(element, list):
            if len(element) == 1:  # 判断key是否存在
                # logger.debug('len(element) == 1')
                brk = False
                for o in json_dict:
                    if element[0] in o.keys():
                        json_dict = o[element[0]]
                        logger.debug(
                            "json_dict update: type: "
                            + str(type(json_dict))
                            + " len: "
                            + str(len(json_dict))
                        )
                        brk = True
                        break
                if brk is False:
                    return ""  # 如果没有匹配到，返回空字符串
            elif len(element) == 2:  # value值和给定值匹配
                # logger.debug('len(element) == 2')
                brk = False
                for o in json_dict:
                    if o[element[0]] == element[1]:
                        json_dict = o
                        logger.debug(
                            "json_dict update: type: "
                            + str(type(json_dict))
                            + " len: "
                            + str(len(json_dict))
                        )
                        brk = True
                        break
                if brk is False:
                    return ""  # 如果没有匹配到，返回空字符串
                # return('')  # 如果没有匹配到，返回空字符串
            elif len(element) == 3:
                # logger.debug('len(element) == 3')
                # ['detail','CONTAINS','3个月身份证关联家庭地址数'],['detail','REGEXP','\d$']
                # logger.debug("-------------------------"+str(element))
                if element[1] == "CONTAINS":
                    # logger.debug("-------------------------")
                    brk = False
                    for o in json_dict:
                        if element[2] in o[element[0]]:
                            json_dict = o
                            logger.debug(
                                "json_dict update: type: "
                                + str(type(json_dict))
                                + " len: "
                                + str(len(json_dict))
                            )
                            brk = True
                            break
                    if brk is False:
                        return ""  # 如果没有匹配到，返回空字符串
                if element[1] == "GETLIST" and isinstance(element[2], int):
                    json_dict = json_dict.get(element[0], {})[element[2]]
                    logger.debug(
                        "json_dict update: type: "
                        + str(type(json_dict))
                        + " len: "
                        + str(len(json_dict))
                    )
                elif element[1] == "GETLIST" and isinstance(element[2], str):
                    json_dict = json_dict.get(element[0], {})
                    brk = False
                    for o in json_dict:
                        if isinstance(o, str):
                            # print(element[2]+'-000000000000000000000'+o)
                            m = re.search(element[2], o)
                            if m is None:
                                continue
                            else:
                                json_dict = m.group()
                                logger.debug(
                                    "json_dict update: type: "
                                    + str(type(json_dict))
                                    + " len: "
                                    + str(len(json_dict))
                                )
                                brk = True
                                break
                    if brk is False:
                        return ""  # 如果没有匹配到，返回空字符串
    return json_dict


def flatten(f, conf_dict):
    """
    input json str
    flatten json and return sql
    """
    if isinstance(f, str):
        json = js.loads(f)
    elif isinstance(f, dict):
        json = f
    else:
        json = js.load(f)

    row = {}
    for key in conf_dict:
        logger.debug("handle column: " + key)
        row[key] = drill(json, conf_dict[key])

    # 转换成str
    for key in row:
        row[key] = str(row[key])

    return row


if __name__ == "__main__":
    pass
