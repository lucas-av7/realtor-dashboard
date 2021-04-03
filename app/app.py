from images import bp_images
from password import bp_password
from products import bp_products
from store import bp_store
from categories import bp_categories
from users import bp_users
from profile import bp_profile
from purposes import bp_purposes
from flask import Flask, render_template
from flask_mysqldb import MySQL
from flask_mail import Mail
import os
from decorators import is_logged_in

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

# Config MySql
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DB")
app.config['MYSQL_UNIX_SOCKET'] = os.environ.get("MYSQL_UNIX_SOCKET")
app.config['MYSQL_CURSORCLASS'] = os.environ.get("MYSQL_CURSORCLASS")

# Config Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

# Init MySQL
mysql = MySQL(app)
app.db = mysql

# Init Mail
mail = Mail(app)
app.mail = mail

# Home page


@app.route('/painel-admin')
def home():
    return render_template('home.html')


# Dashboard
@app.route('/painel-admin/dashboard')
@is_logged_in  # Check if the user is logged in
def dashboard():
    return render_template('dashboard.html')


# Blueprints
app.register_blueprint(bp_users)
app.register_blueprint(bp_categories)
app.register_blueprint(bp_purposes)
app.register_blueprint(bp_store)
app.register_blueprint(bp_products)
app.register_blueprint(bp_images)
app.register_blueprint(bp_password)
app.register_blueprint(bp_profile)
