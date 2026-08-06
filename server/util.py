import json
import pickle
import numpy as np
from pathlib import Path
__location=None
__data_column=None
__model=None


def get_estimated_price(location,sqft,bhk,bath):
    try:
        loc_index = __data_column.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_column))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk

    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0],2)


def get_location_names():
    return __location

def load_saved_artifacts():
    print("loading saved artifacts")
    global __location
    global __data_column

    artifact_dir = Path(__file__).resolve().parent / "Artifact"
    with open(artifact_dir / "columns.json", "r") as f:
        __data_column = json.load(f)["data_columns"]
        __location = __data_column[3:]

    global __model
    with open(artifact_dir / "Bengaluru_Home_Prices_Model.pickle", "rb") as f:
        __model = pickle.load(f)

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2))  # other location
    print(get_estimated_price('Ejipura', 1000, 2, 2))