from sachima.main_runner import run
from sachima.filter_enum import FilterEnum as _
from sachima.params import Filter
from services.db_connects import db

db = db()


def main(api_params={}):

    PARAM_IN = {"handler": "hello", "params": {"行数": 40}, "filters": []}
    return run(PARAM_IN, api_params)


if __name__ == "__main__":
    # testing
    res = main()
    print(res)
    # pass
