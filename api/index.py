from pathlib import Path
import json
import pickle

import numpy as np
from flask import Flask, jsonify, request

app = Flask(__name__)

__location = None
__data_column = None
__model = None


def load_saved_artifacts():
    global __location
    global __data_column
    global __model

    artifact_dir = Path(__file__).resolve().parent / "Artifact"
    with open(artifact_dir / "columns.json", "r") as f:
        __data_column = json.load(f)["data_columns"]
        __location = __data_column[3:]

    with open(artifact_dir / "Bengaluru_Home_Prices_Model.pickle", "rb") as f:
        __model = pickle.load(f)


load_saved_artifacts()


def get_estimated_price(location, sqft, bhk, bath):
    try:
        loc_index = __data_column.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_column))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0], 2)


def get_location_names():
    return __location


@app.get("/api/get_location_names")
def get_location_names_route():
    return jsonify({"locations": get_location_names()})


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

        estimated_price = get_estimated_price(location, total_sqft, bhk, bath)
        return jsonify({"estimated_price": estimated_price})
    except Exception as exc:
        return jsonify({"error": str(exc), "received_data": data}), 400


@app.get("/")
def health_check():
    return jsonify({"status": "ok"})
