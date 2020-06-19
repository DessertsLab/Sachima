import os
import functools
import time
import sachima.sns as sns
import datetime
from sachima.log import logger
from sachima import conf
import inspect


def only_in_night(func):
    """this task can only run in 19:00 to 22:00"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 7 <= datetime.datetime.now().hour < 22:
            logger.info("this task can only run in 19:00 to 22:00")
            return {}
        else:
            return func(*args, **kwargs)

    return wrapper


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
        file_name = os.path.basename(inspect.getsourcefile(func))
        time_str = str(datetime.datetime.now())
        try:
            t = SENDING_STR.format(file_name, time_str)
            sns.send_dingding(t, t, INFO_GRP_TOKEN)
            value = func(*args, **kwargs)
            return value
        except Exception as ex:
            title = ERRSENT_STR.format(file_name, time_str)
            exception_info = str(ex)
            sns.send_dingding(title, title + exception_info, ERROR_GRP_TOKEN)
            # sns.send_dingding(title, title + exception_info, INFO_GRP_TOKEN)
            logger.info(ex)
            raise ex

    return wrapper


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        # logger.info(f"Finished {inspect.getfile(func)} in {run_time:.4f} secs")
        logger.info(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer


def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]  # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)  # 3
        logger.info(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        logger.info(f"{func.__name__!r} returned {value!r}")  # 4
        return value

    return wrapper_debug


def slow_down(func):
    """Sleep 1 second before calling the function"""

    @functools.wraps(func)
    def wrapper_slow_down(*args, **kwargs):
        time.sleep(1)
        return func(*args, **kwargs)

    return wrapper_slow_down


def singleton(cls):
    """Make a class a Singleton class (only one instance)"""

    @functools.wraps(cls)
    def wrapper_singleton(*args, **kwargs):
        if not wrapper_singleton.instance:
            wrapper_singleton.instance = cls(*args, **kwargs)
        return wrapper_singleton.instance

    wrapper_singleton.instance = None
    return wrapper_singleton


def clock(func):
    @functools.wraps(func)
    def wrapper_clock(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(", ".join(repr(arg) for arg in args))
        if kwargs:
            pairs = ["%s=%r" % (k, w) for k, w in sorted(kwargs.items())]
            arg_lst.append(", ".join(pairs))
        arg_str = ", ".join(arg_lst)
        logger.info("[%0.8fs] %s(%s) => %r" % (elapsed, name, arg_str, result))
        return result

    return wrapper_clock
