from sachima.send import send
from sachima.api import api
from sachima.tools import clock
from sachima.scheduler import only_in_night
from sachima.main_runner import run
from sachima.filter_enum import FilterEnum as _
from sachima.params import Filter
from services.db_connects import db

db = db()


# @only_in_night
# @clock
# @send
# @api(platform="superset", isRun=False, name="城市距离", type_="rpc")
def main(api_params={}):

    PARAM_IN = {
        # "model": [
        #     ("email_content_style_example.sql", db.ENGINE_MYSQL_duckchat)
        # ],
        "handler": "hello",
        "params": {"行数": 40},
        "filters": [],
    }
    return run(PARAM_IN, api_params)


if __name__ == "__main__":
    # testing
    res = main()
    print(res)
    # pass
