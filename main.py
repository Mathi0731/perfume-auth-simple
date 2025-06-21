from flask import Flask
from app.routes_simple import simple
import pymysql
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ✅ Environment variables for Railway MySQL
db_config = {
    "host": os.getenv("MYSQLHOST"),
    "user": os.getenv("MYSQLUSER"),
    "password": os.getenv("MYSQLPASSWORD"),
    "database": os.getenv("MYSQLDATABASE"),
    "port": int(os.getenv("MYSQLPORT")),
    "cursorclass": pymysql.cursors.DictCursor
}

# ✅ Function to create DB connection
def get_db_connection():
    return pymysql.connect(**db_config)

# Attach to app context
app.config["get_db_connection"] = get_db_connection

# Register blueprint
app.register_blueprint(simple)

if __name__ == '__main__':
    app.run(debug=True)
