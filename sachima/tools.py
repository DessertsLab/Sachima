import functools
import time
import inspect


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()  # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()  # 2
        run_time = end_time - start_time  # 3
        print(f"Finished {inspect.getfile(func)} in {run_time:.4f} secs")
        return value

    return wrapper_timer


def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]  # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)  # 3
        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")  # 4
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


class Averager:
    def __init__(self):
        self.series = []

    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total / len(self.series)


def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total  # 自由变量 闭包
        count += 1
        total += new_value
        return total / count

    return averager


def clock(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
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
        print("[%0.8fs] %s(%s) => %r" % (elapsed, name, arg_str, result))
        return result

    return wrapper


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


def tools_extract(df, p, *cols):
    for c in cols:
        filter_list = p.get(c, None)
        if p.get(c, None) == "" or p.get(c, None) is None:
            continue
        if isinstance(p.get(c, None), str):
            filter_list = [filter_list]
        if filter_list:
            print(df)
            print("---------c------")
            print(c)
            print(filter_list)
            df = df[df[c].isin(filter_list)]
    return df
