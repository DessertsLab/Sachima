from flask import Flask, jsonify, request
import json

from sachima.rpc import Data
from sachima import conf

CONFIG = conf.get("BROKER")

app = Flask(__name__)


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
def sachima():
    print(request.json)
    return jsonify(sachima_rpc_reports(request))

