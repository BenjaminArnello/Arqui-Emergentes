import sqlite3

def get_db():
    conn = sqlite3.connect('iot.db')
    return conn

def create_tables():
    tables = [
        """CREATE TABLE IF NOT EXISTS admin (
                username TEXT PRIMARY KEY NOT NULL,
                password TEXT NOT NULL
            )
        """,

        """CREATE TABLE IF NOT EXISTS company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_username TEXT UNIQUE NOT NULL,
            company_name TEXT NOT NULL,
            company_api_key TEXT NOT NULL,
            FOREIGN KEY (admin_username) REFERENCES admin(username)
        )
        """,

        """CREATE TABLE IF NOT EXISTS location (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            location_name TEXT NOT NULL,
            location_country TEXT NOT NULL,
            location_city TEXT NOT NULL,
            location_meta TEXT,
            FOREIGN KEY (company_id) REFERENCES company(id)
        )
        """,

        """CREATE TABLE IF NOT EXISTS sensor (
            sensor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            location_id INTEGER NOT NULL,
            sensor_name TEXT NOT NULL,
            sensor_category TEXT NOT NULL,
            sensor_meta TEXT,
            sensor_api_key TEXT NOT NULL,
            FOREIGN KEY (location_id) REFERENCES location(id)
        )
        """,

        """CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sensor_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (sensor_id) REFERENCES sensor(sensor_id)
        )
        """
    ]
    
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
    
    db.commit()
    db.close()


