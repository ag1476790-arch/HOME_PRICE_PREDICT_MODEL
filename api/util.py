import json
import pickle
import numpy as np
from pathlib import Path

__location = None
__data_column = None
__model = None


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


def load_saved_artifacts():
    print("loading saved artifacts")
    global __location
    global __data_column
    global __model

    artifact_dir = Path(__file__).resolve().parent / "Artifact"
    with open(artifact_dir / "columns.json", "r") as f:
        __data_column = json.load(f)["data_columns"]
        __location = __data_column[3:]

    with open(artifact_dir / "Bengaluru_Home_Prices_Model.pickle", "rb") as f:
        __model = pickle.load(f)
