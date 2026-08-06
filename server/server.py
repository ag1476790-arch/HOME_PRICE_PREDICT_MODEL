from flask import Flask, request, jsonify
import util

app = Flask(__name__)


util.load_saved_artifacts()


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():

    # Try form data first
    data = request.form.to_dict()

    # If no form data, try JSON
    if not data:
        data = request.get_json(silent=True) or {}

    print("RECEIVED DATA:", data)

    try:
        total_sqft = float(data['total_sqft'])
        location = data['location']
        bhk = int(data['bhk'])
        bath = int(data['bath'])

        estimated_price = util.get_estimated_price(
            location,
            total_sqft,
            bhk,
            bath
        )

        response = jsonify({
            'estimated_price': estimated_price
        })

        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        return jsonify({
            'error': str(e),
            'received_data': data
        }), 400


if __name__ == "__main__":
    print("Starting Flask Server...")
    app.run(debug=True)