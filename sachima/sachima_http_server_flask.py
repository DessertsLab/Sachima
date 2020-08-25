from flask import Flask, jsonify, request, render_template
import os

from sachima.rpc import Data
from sachima import conf

CONFIG = conf.get("BROKER")

app = Flask(
    __name__,
    static_folder=os.path.join("assets", "static"),
    template_folder=os.path.join("assets"),
)


def sachima_rpc_reports(req, local=True):
    print("*" * 80)
    print(req.json)
    d = Data()
    res = d.get_report(req.json)

    # TODO: is Waffle call me twice? improve it
    if req.json.get("dataonly") == "True":
        return {
            "dataSource": res.get("dataSource", []),
            "columns": res.get("columns", []),
        }
    else:
        return res


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/reports", methods=["POST"])
def sachima():
    # print(request.json)
    return jsonify(sachima_rpc_reports(request))
