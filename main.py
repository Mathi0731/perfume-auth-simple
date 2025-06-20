from flask import Flask
from app.routes_simple import simple

# ✅ Patch PyMySQL to act like MySQLdb
import pymysql
pymysql.install_as_MySQLdb()

from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ✅ Railway-compatible MySQL environment variables
import os
app.config['MYSQL_HOST'] = os.getenv('MYSQLHOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('MYSQLUSER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQLPASSWORD', '1234')
app.config['MYSQL_DB'] = os.getenv('MYSQLDATABASE', 'perfume_auth')
app.config['MYSQL_PORT'] = int(os.getenv('MYSQLPORT', 3306))  # Optional but safer

# Initialize MySQL and assign to app context
mysql = MySQL(app)
app.mysql = mysql

# Register Blueprint routes
app.register_blueprint(simple)

if __name__ == '__main__':
    app.run(debug=True)
