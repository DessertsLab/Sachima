import sachima.handler as han
from sachima.model import Data


def rpts_controller(model_in, h_er):
    res_df = h_er.handle(model_in)
    return res_df


def run(p_in, api_params):
    if api_params == {}:
        print('empty api_params-----------------------------')

    if p_in['params'] == {}:
        print('empty user_params-----------------------------')

    if 'model' in p_in and p_in['model']:
        data_in = [
            Data(dataname,
                 source,
                 p_in['params'],
                 api_params).data for dataname, source in p_in['model']
        ]
    else:
        data_in = None
    handler = han.ReportsHandler(handler=p_in['handler'])
    return rpts_controller(data_in, handler)
