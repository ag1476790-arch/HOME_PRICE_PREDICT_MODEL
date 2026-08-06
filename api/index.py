from pathlib import Path
import sys

from flask import Flask, jsonify, request

sys.path.append(str(Path(__file__).resolve().parent.parent / "server"))

import util

app = Flask(__name__)
util.load_saved_artifacts()


@app.get("/api/get_location_names")
def get_location_names():
    return jsonify({"locations": util.get_location_names()})


@app.post("/api/predict_home_price")
def predict_home_price():
    data = request.form.to_dict()
    if not data:
        data = request.get_json(silent=True) or {}

    try:
        total_sqft = float(data["total_sqft"])
        location = data["location"]
        bhk = int(data["bhk"])
        bath = int(data["bath"])

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        return jsonify({"estimated_price": estimated_price})
    except Exception as exc:
        return jsonify({"error": str(exc), "received_data": data}), 400


@app.get("/")
def health_check():
    return jsonify({"status": "ok"})
