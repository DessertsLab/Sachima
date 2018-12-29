import sachima.sns as sns
import datetime
import yaml


def send(func):
    '''
    send msg to sns app called dingding
    https://open-doc.dingtalk.com/docs/doc.htm?spm=a219a.7629140.0.0.2vzwCr&treeId=257&articleId=105735&docType=1
    you should conif your token in sachima.yaml
    '''
    ERROR_GRP_TOKEN = ''
    INFO_GRP_TOKEN = ''

    with open('conf/sachima.yaml', 'r') as f:
        c = yaml.load(f)
        ERROR_GRP_TOKEN = c['sns']['dingding']['ERROR_GRP_TOKEN']
        INFO_GRP_TOKEN = c['sns']['dingding']['INFO_GRP_TOKEN']
        SENDING_STR = c['sns']['dingding']['SENDING_STR']
        ERRSENT_STR = c['sns']['dingding']['ERRSENT_STR']

    def wrapper(a):
        try:
            time_str = str(datetime.datetime.now())
            t = SENDING_STR.format(a['handler'], time_str)
            sns.send_dingding(t, t, ERROR_GRP_TOKEN)
            return func(a)
        except Exception as ex:
            title = ERRSENT_STR.format(
                a['handler'],
                str(datetime.datetime.now())
            )
            data = str(ex)
            sns.send_dingding(title, title + data, ERROR_GRP_TOKEN)
            sns.send_dingding(
                title, title + data,
                INFO_GRP_TOKEN
            )

    return wrapper
