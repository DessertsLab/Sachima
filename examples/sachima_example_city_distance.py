from sachima.main_runner import run
from sachima.filter_enum import FilterEnum as _
from sachima.params import Filter


def main(api_params={}):
    city_from = (_.TYPE.ITEMSELECT, {"option": "出发城市"})
    city_to = (_.TYPE.ITEMSELECT, {"option": "终点城市"})
    set_lines = (
        _.TYPE.ITEMSELECT,
        _.PROPS.ALLOWCLEAR.TRUE,
        {"option": list(range(0, 300000, 100))},
    )

    city_from = Filter("出发城市", setter=city_from)
    city_to = Filter("终点城市", setter=city_to)
    yourlines = Filter("行数", setter=set_lines)

    PARAM_IN = {
        "handler": "city_distance",
        "params": {"行数": 30},
        "filters": [city_from, city_to, yourlines],
    }
    return run(PARAM_IN, api_params)


if __name__ == "__main__":
    res = main()
