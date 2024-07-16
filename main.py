from flask import Flask, request, jsonify
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

@app.route("/api/v1/get_locations/<id>", methods=["GET"])
def get_locations(id):
    print("entra")
    locations = functions.get_locations(id)
    return jsonify(locations)




if __name__ == "__main__":

    create_tables()
    app.run(debug=False)