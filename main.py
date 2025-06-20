from flask import Flask
from app.routes_simple import simple
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ✅ MySQL config — replace these with Railway values if needed
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'perfume_auth'

# Initialize MySQL and assign to app context
mysql = MySQL(app)
app.mysql = mysql  # ← this makes it accessible from routes

# Register your Option A routes
app.register_blueprint(simple)

if __name__ == '__main__':
    app.run(debug=True)
