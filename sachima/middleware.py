from sachima.filter_enum import FilterEnum as _
from sachima.params import Filter

def append_select_filter(mainrunner_json_result, filters):
    '''
    add filters to main_runner results \n
    usage: append_select_filter(return_res_from_main,[{"name":"行纬度","option":[]},{"name":"列纬度","option":[]}] ) 
    '''
    for f in filters:
        mainrunner_json_result["filters"].append(
           Filter(
                f.get("name"),
                setter=(
                    _.TYPE.ITEMSELECT,
                    _.PROPS.ALLOWCLEAR.TRUE,
                    _.PROPS.MODE.MULTIPLE,
                    {"option": f.get("option")},
                ),
            ), 
        )
