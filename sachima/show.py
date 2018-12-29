def show(func):
    def wrapper(a):
        try:
            print('show had been called')
            return func(a)
        except Exception as ex:
            print('Exception show called')

    return wrapper
