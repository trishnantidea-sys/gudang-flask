from flask import Flask, jsonify, request
import mysql.connector
import hashlib
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables from the .env file (if present)
load_dotenv()

conn = mysql.connector.connect(**{
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PASSWORD'),
    "host": os.getenv('DB_HOST'),
    "database": os.getenv('DB_SCHEMA'),
})
cursor = conn.cursor()

@app.route('/')
def root():
    response = {
        "message" : "gudang-flask API",
        "status" : 200,
        "data" : []
    }

    return jsonify(response)

@app.route('/login', methods=['POST'])
def login():
    # ambil JSON dari body POST
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    password_hash = hashlib.md5(password.encode()).hexdigest()

    query_check = "SELECT id, nama FROM users WHERE email=%s AND password=%s"
    cursor.execute(query_check, (email, password_hash))
    row = cursor.fetchone()

    data = []
    if row is not None:
        id, nama = row

        message = "Success"
        status_code = 200
        data.append({
            "id": id,
            "email": email,
            "nama": nama
        })
    else:
        message = "Unauthorized"
        status_code = 401
    
    return jsonify({
        "message" : message,
        "status" : status_code,
        "data" : data
    })

app.run(debug=True)