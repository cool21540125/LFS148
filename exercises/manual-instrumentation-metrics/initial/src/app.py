# pyright: reportMissingTypeStubs=false, reportUnknownParameterType=false, reportMissingParameterType=false, reportUnknownArgumentType=false, reportUnknownMemberType=false, reportAttributeAccessIssue=false

import time

import requests
from client import ChaosClient, FakerClient
from flask import Flask, make_response, request, Response

from metric_utils import create_meter, create_request_instruments


# global variables
app = Flask(__name__)
meter = create_meter("app.py", "0.1")


@app.route("/users", methods=["GET"])
def get_user():
    user, status = db.get_user(123)
    data = {}
    if user is not None:
        data = {"id": user.id, "name": user.name, "address": user.address}
    response = make_response(data, status)
    return response


@app.before_request
def before_request_func():
    request_instruments["traffic_volume"].add(
        1, attributes={"http.route": request.path}
    )


@app.after_request
def after_request_func(response: Response) -> Response:
    # ...
    request_instruments["error_rate"].add(1, {
            "http.route": request.path,
            "state": "success" if response.status_code < 400 else "fail",
        }
    )
    return response


def do_stuff():
    time.sleep(0.1)
    url = "http://localhost:6000/"
    response = requests.get(url)
    return response


@app.route("/", methods=["GET", "POST"])
def index():
    do_stuff()
    current_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())
    return f"Hello, World! It's currently {current_time}"


if __name__ == "__main__":
    request_instruments = create_request_instruments(meter)
    db = ChaosClient(client=FakerClient())
    app.run(host="0.0.0.0", debug=True)
