import sqlite3
import os
import json # Make sure to import json at the top of db_manager.py if not there

DB_PATH = os.path.join("data", "storage.db")

def init_db():
    """Initializes the SQLite database and creates tables if they don't exist."""
    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table for storing client details
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            contact_number TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Table for storing the land measurements linked to clients
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS land_measurements (
            measurement_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            land_name TEXT NOT NULL,
            area_sq_meters REAL,
            perimeter_meters REAL,
            raw_coordinates TEXT NOT NULL, -- Will store stringified JSON array
            measured_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (client_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

# Helper function to execute simple fetch queries
def fetch_all(query, parameters=()):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, parameters)
    rows = cursor.fetchall()
    conn.close()
    return rows



def save_measurement_to_db(land_name, area_sqm, perimeter_m, raw_coords):
    """Inserts a new land measurement record into the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Convert the list of coordinates into a JSON string for storage
        coords_string = json.dumps(raw_coords)
        
        cursor.execute('''
            INSERT INTO land_measurements (land_name, area_sq_meters, perimeter_meters, raw_coordinates)
            VALUES (?, ?, ?, ?)
        ''', (land_name, area_sqm, perimeter_m, coords_string))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Database Error: {e}")
        return False
    finally:
        conn.close()


def get_all_measurements():
    """Fetches all saved land measurements from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Fetch data, ordered by newest first
        cursor.execute('''
            SELECT measurement_id, land_name, area_sq_meters, perimeter_meters, measured_at 
            FROM land_measurements 
            ORDER BY measured_at DESC
        ''')
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        print(f"Fetch Error: {e}")
        return []
    finally:
        conn.close()

def delete_measurement(measurement_id):
    """Deletes a specific measurement by its ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM land_measurements WHERE measurement_id = ?', (measurement_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Delete Error: {e}")
        return False
    finally:
        conn.close()