from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_mysqldb import MySQL
import os
from form_class.register_form import RegisterForm
from passlib.hash import sha256_crypt
from decorators.logged import is_logged_in

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
@app.route('/painel-admin/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST'and form.validate():
        name = form.name.data
        email = form.email.data
        password = sha256_crypt.hash(str(form.password.data))
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
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


# User Login
@app.route('/painel-admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']
        
        # Create cursor
        cur = mysql.connection.cursor()
        
        # Get user by username
        result = cur.execute('SELECT * FROM users WHERE email = %s', [email])
        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']
            name = data['name']
            user_id = data['id']
            
            # Compare passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['email'] = email
                session['name'] = name
                session['user_id'] = user_id
                
                flash('Você está logado!', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Usuário ou senha inválido'
                return render_template('login.html', error=error)
        else:
            error = 'Usuário ou senha inválido'
            return render_template('login.html', error=error)
        
        # Close connection
        cur.close()
    
    return render_template('login.html')


# Dashboard
@app.route('/painel-admin/dashboard')
@is_logged_in # Check if the user is logged in
def dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.secret_key=os.environ.get("SECRET_KEY")
    app.run(debug=os.environ.get("FLASK_DEBUG"))