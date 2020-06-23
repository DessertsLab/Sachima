import hashlib
import operator
import pandas as pd
import datetime
from sachima.log import logger


def lengthOfLongestSubstring(s):
    """
    :type s: str
    :rtype: int
    """
    stub = -1
    max_len = 0
    cache = {}

    for i, v in enumerate(s):
        if v in cache and cache[v] > stub:
            stub = cache[v]
            cache[v] = i
        else:
            cache[v] = i
            if i - stub > max_len:
                max_len = i - stub
    return max_len


def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
        for y in range(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest : x_longest], x_longest


def extract(df, p, *cols):
    """
    用cols中的参数名从p中提取参数并过滤df
    如果参数不存在 提取下一个 直到结束
    """
    for c in cols:
        try:
            theparam = p.get(c, None)
        except KeyError:
            logger.info("params {} not exists get next...".format(c))
            theparam = None
        except Exception as ex:
            raise ex

        logger.info("extract {} by {} : {}".format(type(df), c, str(theparam)))
        if theparam == "" or theparam is None or theparam == []:
            logger.info("empty param continue...")
            continue
        # if isinstance(theparam, list):
        #     df = df[df[c].isin(theparam)]
        # if isinstance(theparam, str):
        # handle frontend param 2019-01-17T00:10:00.000Z
        if len(df) == 0:
            break
        if type(df[c].iloc[0]) is datetime.date:
            theparam = _to_date_list(theparam)
            df = df[(df[c] >= theparam[0]) & (df[c] <= theparam[1])]
        elif type(df[c].iloc[0]) is pd.Timestamp:
            if isinstance(theparam, list):
                day_begin = pd.Timestamp(theparam[0])
                day_end = pd.Timestamp(theparam[1])
                df = df[(df[c] >= day_begin) & (df[c] <= day_end)]
            else:
                day_begin = pd.Timestamp(theparam).floor(freq="D")
                day_end = pd.Timestamp(theparam).ceil(freq="D")
                df = df[(df[c] >= day_begin) & (df[c] <= day_end)]
        elif isinstance(theparam, list):
            df = df[df[c].isin(theparam)]
        else:
            df = df[df[c].isin([theparam])]
        logger.info("data remain {} lines".format(str(len(df))))
    return df


def _to_date_list(p):
    if type(p) is pd.Timestamp:
        return [p.date(), p.date()]
    elif isinstance(p, list):
        return [pd.Timestamp(val).date() for val in p]
    elif isinstance(p, str):
        return [pd.Timestamp(p).date(), pd.Timestamp(p).date()]


class Tools:
    @classmethod
    def get_md5_value(cls, s):
        myMd5 = hashlib.md5()
        myMd5.update(s.encode("utf8"))
        myMd5_Digest = myMd5.hexdigest()
        return myMd5_Digest

    @classmethod
    def special_char_remove(self, s):
        """
        特殊字符替换处理函数, 在windows下这些字符无法在文件名中存在
        """
        return (
            s.replace(",", " ").replace("<", "小于").replace(">", "大于").replace("*", "_")
        )

    @classmethod
    def get_truth(cls, inp, relate, cut):
        ops = {
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
            "=": operator.eq,
        }
        return ops[relate](inp, cut)

    @classmethod
    def maybe_float(cls, s):
        try:
            return float(s)
        except (ValueError, TypeError):
            return s

    @classmethod
    def excel_colnum_string(cls, n):
        string = ""
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            string = chr(65 + remainder) + string
        return string


# if __name__ == "__main__":
# YEAR = 2017
# MONTH = 1
# DAY = 1
# HOUR = 12
# MINUTES = 12
# SECONDS = 12

# case1 = (
#     pd.Timestamp(YEAR, MONTH, DAY),
#     [datetime.date(YEAR, MONTH, DAY)],
#     "#1 single timestamp input",
# )
# case2 = (
#     pd.Timestamp(YEAR, MONTH, DAY, HOUR, MINUTES, SECONDS),
#     [datetime.date(YEAR, MONTH, DAY)],
#     "#2 single timestamp input with time",
# )
# case3 = (
#     [pd.Timestamp(YEAR, MONTH, DAY)],
#     [datetime.date(YEAR, MONTH, DAY)],
#     "#3 single timestamp list",
# )
# case4 = (
#     [pd.Timestamp(YEAR, MONTH, DAY), pd.Timestamp(YEAR, MONTH + 1, DAY)],
#     [datetime.date(YEAR, MONTH, DAY), datetime.date(YEAR, MONTH + 1, DAY)],
#     "#4 multi timestamp list",
# )
# case5 = (
#     [
#         pd.Timestamp(YEAR, MONTH, DAY),
#         "{}-{}-{}".format(str(YEAR), str(MONTH + 1), str(DAY)),
#     ],
#     [datetime.date(YEAR, MONTH, DAY), datetime.date(YEAR, MONTH + 1, DAY)],
#     "#5 mix timestamp and str list",
# )
# case6 = (
#     [
#         pd.Timestamp(YEAR, MONTH, DAY),
#         "boom!{}-{}-{}".format(str(YEAR), str(MONTH + 1), str(DAY)),
#     ],
#     [datetime.date(YEAR, MONTH, DAY), datetime.date(YEAR, MONTH + 1, DAY)],
#     ValueError,
# )

# tests = [case1, case2, case3, case4, case5, case6]

# for t in tests:
#     print(_to_date_list(t[0]))
#     assert _to_date_list(t[0]) == t[1], "{} not correct".format(t[2])

# print(longest_common_substring("曝光:不要..._新浪博客", "曝光:人|..."))
