from flask import Flask, request, jsonify, make_response
from base import get_db, create_tables 
import functions as functions


app = Flask(__name__)

@app.route('/')
def index():
    return 'hello world'

@app.route('/api/v1/create_admin', methods = ["POST"])
def insert_admin():
    admin_details = request.get_json()
    username = admin_details["username"]
    password = admin_details["password"]
    result = functions.create_admin(username, password)
    return jsonify(result)

@app.route('/api/v1/create_company', methods = ["POST"])
def insert_company():
    company_details = request.get_json()
    username = company_details["username"]
    companyName = company_details["companyName"]
    result = functions.create_company(username, companyName)
    return jsonify(result)

@app.route('/api/v1/create_location', methods = ["POST"])
def insert_location():
    location_details = request.get_json()
    api_key = location_details["api_key"]
    name = location_details["name"]
    country = location_details["country"]
    city = location_details["city"]
    meta = location_details["meta"]

    result = functions.create_location(api_key, name, country,city,meta)
    return jsonify(result)

@app.route('/api/v1/get_companies/<id>', methods=["GET"])

def get_companies():

    companies = functions.get_companys(id)
    return jsonify(companies)

@app.route("/api/v1/get_locations/<apikey>", methods=["GET"])
def get_locations(apikey):
    print("entra")
    locations = functions.get_locations(apikey)
    return locations

@app.route("/api/v1/get_location/<id>/<apikey>", methods=["GET"])
def get_location(id,apikey):
    print("entra")
    locations = functions.get_location(id, apikey)
    return locations

@app.route("/api/v1/update_location", methods=["PUT"])
def update_location():
    location_details = request.get_json()
    api_key = location_details["api_key"]
    id = location_details["location_id"]
    name = location_details["name"]
    country = location_details["country"]
    city = location_details["city"]
    meta = location_details["meta"]

    result = functions.update_location(api_key,id, name, country,city,meta)
    return result

@app.route("/api/v1/delete_location", methods=["DELETE"])
def delete_location():
    location_details = request.get_json()
    api_key = location_details["api_key"]
    id = location_details["location_id"]

    result = functions.delete_location(api_key,id)
    return result

@app.route('/api/v1/create_sensor', methods = ["POST"])
def insert_sensor():
    details = request.get_json()
    api_key = details["api_key"]
    location_id = details["location_id"]
    sensor_name = details["sensor_name"]
    sensor_category = details["sensor_category"]
    sensor_meta = details["sensor_meta"]

    result = functions.create_sensor(api_key, location_id, sensor_name, sensor_category, sensor_meta)
    return result
@app.route("/api/v1/get_sensors/<apikey>", methods=["GET"])
def get_sensors(apikey):
    locations = functions.get_sensors(apikey)
    return locations

@app.route("/api/v1/get_sensor/<id>/<apikey>", methods=["GET"])
def get_sensor(apikey,id):
    response = functions.get_sensor(apikey, id)
    return response	

@app.route("/api/v1/update_sensor", methods=["PUT"])
def update_sensor():
    details = request.get_json()
    api_key = details["api_key"]
    sensor_id = details["sensor_id"]
    sensor_name = details["sensor_name"]
    sensor_category = details["sensor_category"]
    sensor_meta = details["sensor_meta"]


    result = functions.update_sensor(api_key,sensor_id, sensor_name, sensor_category, sensor_meta)
    return result

@app.route("/api/v1/delete_sensor", methods=["DELETE"])
def delete_sensor():
    details = request.get_json()
    api_key = details["api_key"]
    id = details["sensor_id"]

    result = functions.delete_sensor(api_key,id)
    return result

@app.route("/api/v1/sensor_data", methods=["POST"])
def add_sensor_data():
    details = request.get_json()

    # Check if all required fields are present
    if not details or "sensor_api_key" not in details or "data" not in details:
        return make_response("Petición malformada", 400)

    sensor_api_key = details["sensor_api_key"]
    data = details["data"]

    result = functions.add_sensor_data(sensor_api_key, data)
    return result

@app.route("/api/v1/sensor_data/<api_key>/<desde>/<hasta>/<sensor_id>", methods=["GET"])
def get_sensor_data(api_key, desde, hasta, sensor_id):

    print(api_key)
    print(desde)
    print(hasta)
    print(sensor_id)
    sensor_id = sensor_id[1:-1]
    sensor_array = sensor_id.split(',')
    print(sensor_array)

    result = functions.get_sensor_data(api_key, desde, hasta, sensor_array)
    return result


    return jsonify("ok")
if __name__ == "__main__":

    create_tables()
    app.run(debug=False)