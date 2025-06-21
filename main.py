from flask import Flask
from app.routes_simple import simple
import pymysql
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ✅ Use Railway environment variables
db_config = {
    "host": os.getenv("MYSQLHOST"),
    "user": os.getenv("MYSQLUSER"),
    "password": os.getenv("MYSQLPASSWORD"),
    "database": os.getenv("MYSQLDATABASE"),
    "port": int(os.getenv("MYSQLPORT", 3306)),  # fallback to 3306
    "cursorclass": pymysql.cursors.DictCursor
}

# ✅ Create reusable DB connection
def get_db_connection():
    return pymysql.connect(**db_config)

app.config["get_db_connection"] = get_db_connection

# ✅ Register your Blueprint
app.register_blueprint(simple)

# ✅ THIS IS CRITICAL: Run Flask on Railway's port
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
