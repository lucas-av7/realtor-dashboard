from flask import Flask, render_template
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# Config MySql
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")
app.config['MYSQL_UNIX_SOCKET'] = os.environ.get("MYSQL_UNIX_SOCKET")
app.config['MYSQL_CURSORCLASS'] = os.environ.get("MYSQL_CURSORCLASS")

# Init MySQL
mysql = MySQL(app)

@app.route('/')
def home():
    return 'home'

if __name__ == '__main__':
    app.secret_key=os.environ.get("SECRET_KEY")
    app.run(debug=os.environ.get("FLASK_DEBUG"))