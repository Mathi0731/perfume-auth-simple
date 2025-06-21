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
    "port": int(os.getenv("MYSQLPORT", 3306)),  # Fallback if unset
    "cursorclass": pymysql.cursors.DictCursor
}

# ✅ Function to create DB connection
def get_db_connection():
    return pymysql.connect(**db_config)

# Attach to app context
app.config["get_db_connection"] = get_db_connection

# Register blueprint
app.register_blueprint(simple)

# ✅ Main runner for Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Important for Railway!
    app.run(host="0.0.0.0", port=port)
