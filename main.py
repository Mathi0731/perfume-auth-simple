from flask import Flask
from app.routes_simple import simple
import pymysql
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# 🧪 Debug print to check if MYSQLPORT is read correctly
print("MYSQLPORT =", os.getenv("MYSQLPORT"))

# ✅ Environment variables for Railway MySQL (with safe port fallback)
db_config = {
    "host": os.getenv("MYSQLHOST"),
    "user": os.getenv("MYSQLUSER"),
    "password": os.getenv("MYSQLPASSWORD"),
    "database": os.getenv("MYSQLDATABASE"),
    "port": int(os.getenv("MYSQLPORT", 3306)),  # Default to 3306 if not set
    "cursorclass": pymysql.cursors.DictCursor
}

# ✅ Function to create DB connection
def get_db_connection():
    return pymysql.connect(**db_config)

# Attach DB function to app context
app.config["get_db_connection"] = get_db_connection

# Register blueprint
app.register_blueprint(simple)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway sets PORT dynamically
    app.run(host="0.0.0.0", port=port)
