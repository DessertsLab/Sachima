from sachima import conf
import sachima.sns as sns
import datetime
import functools


def send(func):
    """
    send msg to sns app called dingding
    https://open-doc.dingtalk.com/docs/doc.htm?spm=a219a.7629140.0.0.2vzwCr&treeId=257&articleId=105735&docType=1
    you should conif your token in sachima.yaml
    """
    ERROR_GRP_TOKEN = conf.get("SNS_DINGDING_ERROR_GRP_TOKEN")
    INFO_GRP_TOKEN = conf.get("SNS_DINGDING_INFO_GRP_TOKEN")
    SENDING_STR = conf.get("SNS_DINGDING_SENDING_STR")
    ERRSENT_STR = conf.get("SNS_DINGDING_ERRSENT_STR")

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            # before
            time_str = str(datetime.datetime.now())
            t = SENDING_STR.format(args[0]["handler"], time_str)
            sns.send_dingding(t, t, ERROR_GRP_TOKEN)
            value = func(*args, **kwargs)
            # after
            return value
        except Exception as ex:
            title = ERRSENT_STR.format(
                args[0]["handler"], str(datetime.datetime.now())
            )
            data = str(ex)
            sns.send_dingding(title, title + data, ERROR_GRP_TOKEN)
            sns.send_dingding(title, title + data, INFO_GRP_TOKEN)

    return wrapper
