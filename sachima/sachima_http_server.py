from nameko.standalone.rpc import ClusterRpcProxy

from sanic import Sanic
from sanic.response import json
from sachima import conf

app = Sanic()

CONFIG = conf.get("BROKER")


def sachima_rpc_reports(req):
    with ClusterRpcProxy(CONFIG) as rpc:
        res = rpc.data.get_report(req.json)
        if req.json.get("dataonly") == "True":
            return {
                "dataSource": res.get("dataSource", []),
                "columns": res.get("columns", []),
            }
        else:
            return res


@app.route("/reports", methods=["POST"])
async def sachima(request):
    #     print(request)
    return json(sachima_rpc_reports(request))
