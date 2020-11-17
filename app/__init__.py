from flask import Flask, render_template, request, flash
from flask_mysqldb import MySQL
import os
from form_class.register_form import RegisterForm
from passlib.hash import sha256_crypt

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

# Home page
@app.route('/painel-admin')
def home():
    return render_template('home.html')

# User register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST'and form.validate():
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        is_admin = False
        is_partner = True
        is_approved = False

        # Create cursor
        cur = mysql.connection.cursor()
        
        cur.execute('SELECT * FROM users WHERE email = %s', [email])
        duplicate = cur.fetchone()
        if duplicate:
            flash('Este e-mail já está em uso, utilize outro e-mail ou faça login.', 'danger')
            return render_template('register.html', form=form)
        else:
            cur.execute('INSERT INTO users(name, email, password, is_admin, is_partner, is_approved) VALUES (%s, %s, %s, %s, %s, %s)', 
                        (name, email, password, is_admin, is_partner, is_approved))
            
            # Commit to DB and Close connection
            mysql.connection.commit()
            cur.close()
            
            flash('Você se cadastrou com sucesso, faça o login.', 'success')
            return render_template('home.html')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.secret_key=os.environ.get("SECRET_KEY")
    app.run(debug=os.environ.get("FLASK_DEBUG"))