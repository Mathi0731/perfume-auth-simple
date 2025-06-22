from flask import Flask, redirect
from app.routes_simple import simple
import pymysql
import os
from dotenv import load_dotenv

# ✅ Load environment variables from Railway (.env)
load_dotenv()

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to something random for production

# ✅ Get DB config from Railway-provided env variables
db_config = {
    'host': os.getenv('MYSQLHOST'),              # should be mysql.internal
    'user': os.getenv('MYSQLUSER'),              # typically 'root'
    'password': os.getenv('MYSQLPASSWORD'),
    'database': os.getenv('MYSQLDATABASE'),
    'port': int(os.getenv('MYSQLPORT', 3306)),   # default 3306
    'cursorclass': pymysql.cursors.DictCursor
}

# ✅ Define reusable DB connection
def get_db_connection():
    return pymysql.connect(**db_config)

app.config["get_db_connection"] = get_db_connection

# ✅ Register your routes
app.register_blueprint(simple)

# ✅ Add / route to redirect to /simple-add
@app.route('/')
def home_redirect():
    return redirect('/simple-add')

# ✅ Run the app using Railway-provided PORT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
