from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_mysqldb import MySQL
import os
from decorators import is_logged_in

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
app.db = mysql


# Home page
@app.route('/painel-admin')
def home():
    return render_template('home.html')


# Dashboard
@app.route('/painel-admin/dashboard')
@is_logged_in # Check if the user is logged in
def dashboard():
    return render_template('dashboard.html')


# Blueprints
from users import bp_users
app.register_blueprint(bp_users)
from categories import bp_categories
app.register_blueprint(bp_categories)
from store import bp_store
app.register_blueprint(bp_store)


if __name__ == '__main__':
    app.secret_key=os.environ.get("SECRET_KEY")
    app.run(debug=os.environ.get("FLASK_DEBUG"))