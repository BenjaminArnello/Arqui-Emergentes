from base import get_db
import secrets
import bcrypt
import json


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

def get_locations(id):
    db = get_db()
    cursor = db.cursor()
    selectCompany = "SELECT (id) FROM company  WHERE company_api_key = ?"
    cursor.execute(selectCompany, [id])
    companyIdFetch = cursor.fetchall()
    companyId = companyIdFetch[0][0]

    if companyId:
        query = "SELECT * FROM location"

        cursor.execute(query)
        return cursor.fetchall()
    else:
        return "API KEY incorrecta"


def update_user(currentName, newName, newPassword):
    db = get_db()
    cursor = db.cursor()
    statement = "UPDATE admins SET username = ?, password = ?, rate = ? WHERE id = ?"
    cursor.execute(statement, [name, price, rate, id])
    db.commit()
    return True


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