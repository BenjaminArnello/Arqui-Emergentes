from base import get_db
import secrets
import bcrypt
import json
from flask import make_response 
from collections import defaultdict
import time

def create_admin(username, password):
    
    db = get_db()
    cursor = db.cursor()
    bytes = password.encode('utf-8') 
    salt = bcrypt.gensalt() 
    hashed = bcrypt.hashpw(bytes, salt)
    statement = "INSERT INTO admin(username, password) VALUES (?, ?)"
    cursor.execute(statement, [username, hashed])
    db.commit()

    return True



def create_company(username, companyName):
    db = get_db()
    cursor = db.cursor()
    apikey = secrets.token_urlsafe(16)
    statement = "INSERT INTO company(company_name, admin_username, company_api_key) VALUES (?, ?, ?)"
    cursor.execute(statement, [companyName, username, apikey])
    db.commit()
    
    # Obtener el ID del registro recién insertado
    company_id = cursor.lastrowid
    
    # Obtener la fila completa basada en el ID insertado
    query = "SELECT * FROM company WHERE id = ?"
    cursor.execute(query, [company_id])
    company_row = cursor.fetchone()
    
    db.close()
    return company_row

def get_companys():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM company"
    cursor.execute(query)
    return cursor.fetchall()

def create_location(apikey,name, country, city, meta):
    db = get_db()
    cursor = db.cursor()
    selectCompany = "SELECT (id) FROM company  WHERE company_api_key = ?"
    cursor.execute(selectCompany, [apikey])
    companyIdFetch = cursor.fetchall()
    companyId = companyIdFetch[0][0]

    statement = "INSERT INTO location(company_id, location_name, location_country, location_city, location_meta) VALUES (?, ?, ?, ?, ?)"
    cursor.execute(statement, [companyId, name, country, city, meta])
    db.commit()

    return True

def get_locations(apikey):
    db = get_db()
    cursor = db.cursor()
    
    selectCompany = "SELECT id FROM company WHERE company_api_key = ?"
    cursor.execute(selectCompany, [apikey])
    companyIdFetch = cursor.fetchone() 

    if companyIdFetch:
        company_id = companyIdFetch[0]
        # Fetch locations associated with the company ID
        query = "SELECT * FROM location WHERE company_id = ?"
        cursor.execute(query, [company_id])
        locations = cursor.fetchall()

        return make_response(locations, 200)
    else:
        return make_response("API KEY incorrecta", 401)
    
def get_location(id, apikey):
    db = get_db()
    cursor = db.cursor()
    selectCompany = "SELECT (id) FROM company  WHERE company_api_key = ?"
    cursor.execute(selectCompany, [apikey])
    companyIdFetch = cursor.fetchall()

    if companyIdFetch:
        query = "SELECT * FROM location where id = ?"
        cursor.execute(query, id)
        reply = cursor.fetchall()

        return make_response(reply, 200)
    else:
        return make_response("API KEY incorrecta", 401)

def update_location(apikey,id, name, country, city, meta):
    db = get_db()
    cursor = db.cursor()
    statement1 = "SELECT (id) FROM company  WHERE company_api_key = ?"
    cursor.execute(statement1, [apikey])
    companyIdFetch = cursor.fetchall()
    
    if companyIdFetch:
        statement2 = "UPDATE location SET location_name = ?, location_country = ?, location_city = ?, location_meta = ? WHERE id = ?"
        cursor.execute(statement2, [name, country, city, meta, id])
        db.commit()

        return make_response("Ubicación actualizada correctamente", 200)
    else:
        return make_response("API KEY incorrecta", 401)


def delete_location(apikey,id):
    db = get_db()
    cursor = db.cursor()
    statement1 = "SELECT (id) FROM company  WHERE company_api_key = ?"
    cursor.execute(statement1, [apikey])
    companyIdFetch = cursor.fetchall()
    
    if companyIdFetch:
        statement2 = "DELETE FROM location WHERE id = ?"
        cursor.execute(statement2, [id])
        db.commit()

        return make_response("Ubicación eliminada correctamente", 200)
    else:
        return make_response("API KEY incorrecta", 401)

def create_sensor(apikey, locationId, name, category, meta):
    db = get_db()
    cursor = db.cursor()
    statement1 = "SELECT (id) FROM company  WHERE company_api_key = ?"
    cursor.execute(statement1, [apikey])
    companyIdFetch = cursor.fetchall()

    if companyIdFetch:
        apikey = secrets.token_urlsafe(8)
        statement = "INSERT INTO sensor(location_id, sensor_name, sensor_category, sensor_meta, sensor_api_key) VALUES (?, ?, ?,?,?)"
        cursor.execute(statement, [locationId, name, category, meta, apikey])
        db.commit()
            
        # Obtener el ID del registro recién insertado
        company_id = cursor.lastrowid
        
        # Obtener la fila completa basada en el ID insertado
        query = "SELECT * FROM sensor WHERE sensor_id = ?"
        cursor.execute(query, [company_id])
        company_row = cursor.fetchall()

        
        db.close()

        return make_response(company_row, 200)
    
    else:
        return make_response("API KEY incorrecta", 401)





def get_sensors(apikey):
    db = get_db()
    cursor = db.cursor()
    
    selectCompany = "SELECT id FROM company WHERE company_api_key = ?"
    cursor.execute(selectCompany, [apikey])
    companyIdFetch = cursor.fetchone() 

    if companyIdFetch:
        company_id = companyIdFetch[0]
        # Fetch locations associated with the company ID
        query = "SELECT id, location_name FROM location WHERE company_id = ?"
        cursor.execute(query, [company_id])
        locations = cursor.fetchall()

        if locations:
            # Create a dictionary to store location names
            location_dict = {loc[0]: loc[1] for loc in locations}
            location_ids = list(location_dict.keys())
            
            # Prepare the query with placeholders for the location IDs
            query = "SELECT * FROM sensor WHERE location_id IN ({})".format(','.join(['?']*len(location_ids)))
            cursor.execute(query, location_ids)
            sensors = cursor.fetchall()

            # Group sensors by location_id
            grouped_sensors = defaultdict(list)
            for sensor in sensors:
                grouped_sensors[sensor[1]].append(sensor)  # Assuming location_id is the second element in the sensor tuple
            
            # Create the response structure
            response = []
            for loc_id, sensors in grouped_sensors.items():
                response.append({
                    'location_id': loc_id,
                    'location_name': location_dict[loc_id],
                    'sensors': sensors
                })

            return make_response(response, 200)
        else:
            return make_response("No existen ubicaciones para esta compañia", 404)
    else:
        return make_response("API KEY incorrecta", 401)


def get_sensors(apikey):
    db = get_db()
    cursor = db.cursor()
    
    selectCompany = "SELECT id FROM company WHERE company_api_key = ?"
    cursor.execute(selectCompany, [apikey])
    companyIdFetch = cursor.fetchone() 

    if companyIdFetch:
        company_id = companyIdFetch[0]
        # Fetch locations associated with the company ID
        query = "SELECT id, location_name FROM location WHERE company_id = ?"
        cursor.execute(query, [company_id])
        locations = cursor.fetchall()

        if locations:
            # Create a dictionary to store location names
            location_dict = {loc[0]: loc[1] for loc in locations}
            location_ids = list(location_dict.keys())
            
            # Prepare the query with placeholders for the location IDs
            query = "SELECT * FROM sensor WHERE location_id IN ({})".format(','.join(['?']*len(location_ids)))
            cursor.execute(query, location_ids)
            sensors = cursor.fetchall()

            # Group sensors by location_id
            grouped_sensors = defaultdict(list)
            for sensor in sensors:
                grouped_sensors[sensor[1]].append(sensor)  # Assuming location_id is the second element in the sensor tuple
            
            # Create the response structure
            response = []
            for loc_id, sensors in grouped_sensors.items():
                response.append({
                    'location_id': loc_id,
                    'location_name': location_dict[loc_id],
                    'sensors': sensors
                })

            return make_response(response, 200)
        else:
            return make_response("No locations found for the given company", 404)
    else:
        return make_response("API KEY incorrecta", 401)

def get_sensor(apikey, sensor_id):
    db = get_db()
    cursor = db.cursor()
    
    selectCompany = "SELECT id FROM company WHERE company_api_key = ?"
    cursor.execute(selectCompany, [apikey])
    companyIdFetch = cursor.fetchone() 

    if companyIdFetch:
        company_id = companyIdFetch[0]
        query = "SELECT * FROM sensor WHERE sensor_id = ?"


        cursor.execute(query, [sensor_id])
        sensor = cursor.fetchall()

        if sensor:

             location_id = sensor[0][1]

             query2 = "SELECT * FROM location WHERE id = ?"
             cursor.execute(query2, [location_id])
             location = cursor.fetchall()
             

             if location:
                 if location[0][1] == company_id[0]:
                    return make_response(sensor, 200)
             else: return make_response("Este sensor no tiene compañia", 401)
                 
        else:
            return make_response("Esta compañia no tiene acceso a este sensor", 401)
    else:
        return make_response("API KEY incorrecta", 401)


def update_sensor(apikey,sensor_id, name, category, meta):
    db = get_db()
    cursor = db.cursor()
    statement1 = "SELECT (id) FROM company  WHERE company_api_key = ?"
    cursor.execute(statement1, [apikey])
    companyIdFetch = cursor.fetchall()


    if companyIdFetch:
        company_id = companyIdFetch[0]
        query = "SELECT * FROM sensor WHERE sensor_id = ?"
        cursor.execute(query, [sensor_id])
        sensor = cursor.fetchall()

        if sensor:
             location_id = sensor[0][1]
             query2 = "SELECT * FROM location WHERE id = ?"
             cursor.execute(query2, [location_id])
             location = cursor.fetchall()
             

             if location:
                 if location[0][1] == company_id[0]:
                    edit = "UPDATE sensor SET sensor_name = ?, sensor_category = ?, sensor_meta = ? WHERE sensor_id = ?"
                    cursor.execute(edit, [name, category,meta, sensor_id])
                    db.commit()
                    return make_response("Sensor modificado correctamente", 200)
                 else: return make_response("Esta compañia no tiene acceso a este sensor")
             else: return make_response("Este sensor no tiene compañia", 401)
                 
        else:
            return make_response("Este sensor no existe", 401)
    else:
        return make_response("API KEY incorrecta", 401)
    

def delete_sensor(apikey, sensor_id):
    db = get_db()
    cursor = db.cursor()
    
    selectCompany = "SELECT id FROM company WHERE company_api_key = ?"
    cursor.execute(selectCompany, [apikey])
    companyIdFetch = cursor.fetchone() 

    if companyIdFetch:
        company_id = companyIdFetch[0]
        query = "SELECT * FROM sensor WHERE sensor_id = ?"


        cursor.execute(query, [sensor_id])
        sensor = cursor.fetchall()

        if sensor:

             location_id = sensor[0][1]

             query2 = "SELECT * FROM location WHERE id = ?"
             cursor.execute(query2, [location_id])
             location = cursor.fetchall()
             

             if location:
                 if location[0][1] == company_id:
                    edit = "DELETE FROM sensor WHERE sensor_id = ?"
                    cursor.execute(edit, [sensor_id])
                    db.commit()
                    return make_response("Sensor eliminado correctamente", 200)
             else: return make_response("Este sensor no tiene compañia", 401)
                 
        else:
            return make_response("Esta compañia no tiene acceso a este sensor", 401)
    else:
        return make_response("API KEY incorrecta", 401)
    

def add_sensor_data(sensor_api_key, data):
    db = get_db()
    cursor = db.cursor()

    if sensor_api_key is None or data is None:
        return make_response("No se pueden ingresar campos nulos", 400)
    
    selectSensor = "SELECT sensor_id FROM sensor WHERE sensor_api_key = ?"
    cursor.execute(selectSensor, [sensor_api_key])
    sensorIdFetch = cursor.fetchone()


    if sensorIdFetch:
        query = "INSERT INTO sensor_data(sensor_id, data, time) VALUES (?, ?, ?)"
        cursor.execute(query, [sensorIdFetch[0], data, int(time.time())])
        db.commit()
        
        return make_response("Data ingresada correctamente", 201)
    else:
        return make_response("No existe un sensor relacionado a esta API KEY", 400)


def get_sensor_data(api_key, desde, hasta, sensor_id):
    db = get_db()
    cursor = db.cursor()

    if api_key is None or desde is None or hasta is None or sensor_id is None:
        return make_response("La petición contiene campos nulos", 400)

    # Convert sensor_id to a list if it's not already
    if not isinstance(sensor_id, list):
        sensor_id = [sensor_id]

    # Fetch company_id based on api_key
    selectCompany = "SELECT id FROM company WHERE company_api_key = ?"
    cursor.execute(selectCompany, [api_key])
    companyIdFetch = cursor.fetchone()

    if companyIdFetch:
        company_id = companyIdFetch[0]

        # Fetch location ids associated with the company
        query2 = "SELECT id FROM location WHERE company_id = ?"
        cursor.execute(query2, [company_id])
        locationsId = cursor.fetchall()

        if locationsId:
            # Extract location ids into a list
            location_ids = [loc[0] for loc in locationsId]

            # Fetch sensor ids associated with the locations
            query_sensors = "SELECT sensor_id FROM sensor WHERE location_id IN ({})".format(','.join(['?'] * len(location_ids)))
            cursor.execute(query_sensors, location_ids)
            sensor_id_company = cursor.fetchall()
    

            sensor_id_company = [str(sid[0]) for sid in sensor_id_company]

            # Convert fetched sensor ids to sets for intersection
            setSensorCompany = set(sensor_id_company)
            setSensor = set(sensor_id)

            # Find intersection of sensor ids
            filtered = list(setSensorCompany.intersection(setSensor))



            # Fetch sensor data based on filtered sensor ids, desde, and hasta
            query = "SELECT * FROM sensor_data WHERE sensor_id IN ({}) AND time >= ? AND time <= ?".format(','.join(['?'] * len(filtered)))
            cursor.execute(query, filtered + [desde, hasta])
            sensorData = cursor.fetchall()

            return make_response(sensorData, 200)
        else:
            return make_response("No se tiene acceso a ningun sensor", 401)
    else:
        return make_response("API KEY Incorrecta", 401)



def delete_game(id):
    db = get_db()
    cursor = db.cursor()
    statement = "DELETE FROM games WHERE id = ?"
    cursor.execute(statement, [id])
    db.commit()
    return True


def get_by_id(id):
    db = get_db()
    cursor = db.cursor()
    statement = "SELECT id, name, price, rate FROM games WHERE id = ?"
    cursor.execute(statement, [id])
    return cursor.fetchone()


def get_games():
    db = get_db()
    cursor = db.cursor()
    query = "SELECT id, name, price, rate FROM games"
    cursor.execute(query)
    return cursor.fetchall()