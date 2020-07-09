from nameko.standalone.rpc import ClusterRpcProxy

from sanic import Sanic
from sanic.response import json
from sachima import conf

from sachima.rpc import Data

app = Sanic()

CONFIG = conf.get("BROKER")


# TODO: separate local and server mode  local no depends on nameko and redis
def sachima_rpc_reports(req, local=True):
    if local is not True:
        with ClusterRpcProxy(CONFIG) as rpc:
            res = rpc.data.get_report(req.json)
    else:
        d = Data()
        res = d.get_report(req.json)

    if req.json.get("dataonly") == "True":
        return {
            "dataSource": res.get("dataSource", []),
            "columns": res.get("columns", []),
        }
    else:
        return res


@app.route("/reports", methods=["POST"])
async def sachima(request):
    return json(sachima_rpc_reports(request))
