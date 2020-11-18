from flask import Blueprint, current_app, request, flash, render_template, redirect, url_for, session
from decorators import is_logged_in
from passlib.hash import sha256_crypt
from form_class import RegisterForm


bp_users = Blueprint('users', __name__)

# User register
@bp_users.route('/painel-admin/register', methods=['GET', 'POST'])
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
        cur = current_app.db.connection.cursor()
        
        cur.execute('SELECT * FROM users WHERE email = %s', [email])
        duplicate = cur.fetchone()
        if duplicate:
            flash('Este e-mail já está em uso, utilize outro e-mail ou faça login.', 'danger')
            return render_template('register.html', form=form)
        else:
            cur.execute('INSERT INTO users(name, email, password, is_admin, is_partner, is_approved) VALUES (%s, %s, %s, %s, %s, %s)', 
                        (name, email, password, is_admin, is_partner, is_approved))
            
            # Commit to DB and Close connection
            current_app.db.connection.commit()
            cur.close()
            
            flash('Você se cadastrou com sucesso, faça o login.', 'success')
            return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


# User Login
@bp_users.route('/painel-admin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']
        
        # Create cursor
        cur = current_app.db.connection.cursor()
        
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


# User Logout
@bp_users.route('/painel-admin/logout')
@is_logged_in # Check if the user is logged in
def logout():
    session.clear()
    flash('Você saiu com sucesso', 'success')
    return redirect(url_for('users.login'))
