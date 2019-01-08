import sachima.handler as han
from sachima.model import Data


def rpts_controller(model_in, h_er):
    res_df = h_er.handle(model_in)
    return res_df


# def rpts_view(control_in, view):
#     '''
#     todo: output rpts to excel
#     '''
#     res_v = view.vis(control_in)
#     return res_v


def run(p_in):
    if 'model' in p_in and p_in['model']:
        data_in = [
            Data(dataname, source).data for dataname, source in p_in['model']
        ]
    else:
        data_in = None
    handler = han.ReportsHandler(handler=p_in['handler'])
    rpts_controller(data_in, handler)
