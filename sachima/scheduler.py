from datetime import datetime


def only_in_night(func):
    def wrapper(a):
        if 7 <= datetime.now().hour < 22:
            pass
        else:
            func(a)
    return wrapper
