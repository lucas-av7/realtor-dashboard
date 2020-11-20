from flask import Blueprint, current_app, request, flash, render_template, redirect, url_for, session
from decorators import is_logged_in, is_admin_in
from passlib.hash import sha256_crypt
from form_class import RegisterForm, EditUserForm


bp_users = Blueprint('users', __name__)

# User register
@bp_users.route('/painel-admin/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST'and form.validate():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
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
            return render_template('users/register.html', form=form)
        else:
            cur.execute('INSERT INTO users(name, email, phone, password, is_admin, is_partner, is_approved) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                        (name, email, phone, password, is_admin, is_partner, is_approved))
            
            # Commit to DB and Close connection
            current_app.db.connection.commit()
            cur.close()
            
            flash('Você se cadastrou com sucesso, faça o login.', 'success')
            return redirect(url_for('users.login'))

    return render_template('users/register.html', form=form)


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
            is_admin = data['is_admin']
            is_approved = data['is_approved']
            
            # Check if the user is not approved
            if not is_approved:
                error = 'Sua conta ainda não foi aprovada pelo administrador'
                return render_template('users/login.html', error=error)
            # Compare passwords
            elif sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['email'] = email
                session['name'] = name
                session['user_id'] = user_id
                if is_admin:
                    session['is_admin'] = is_admin
                
                flash('Você está logado!', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Usuário ou senha inválido'
                return render_template('users/login.html', error=error)
        else:
            error = 'Usuário ou senha inválido'
            return render_template('users/login.html', error=error)
        
        # Close connection
        cur.close()
    
    return render_template('users/login.html')


# User Logout
@bp_users.route('/painel-admin/logout')
@is_logged_in # Check if the user is logged in
def logout():
    session.clear()
    flash('Você saiu com sucesso', 'success')
    return redirect(url_for('users.login'))


# List users
@bp_users.route('/painel-admin/users')
@is_logged_in # Check if the user is logged in
@is_admin_in
def users():
    # Create cursor
    cur = current_app.db.connection.cursor()
    
    result = cur.execute('SELECT * FROM users WHERE is_partner = True ORDER BY id DESC')
    users = cur.fetchall()
    
    if result > 0:
        return render_template('users/users.html', users=users)
    else:
        error = 'Sem usuários parceiros cadastrados.'
        return render_template('users/users.html', error=error)

    # Close connection
    cur.close()


# Edit users
@bp_users.route('/painel-admin/users/edit_user/<string:id>', methods=['GET', 'POST'])
@is_logged_in # Check if the user is logged in
@is_admin_in
def edit_user(id):
    # Create cursor
    cur = current_app.db.connection.cursor()
    
    # Get user by ID
    cur.execute('SELECT * FROM users WHERE id=%s', [id])
    user = cur.fetchone()
    
    # Get form
    form = EditUserForm(request.form)
    
    # Populate title field
    form.name.data = user['name']
    form.email.data = user['email']
    form.phone.data = user['phone']
    
    if request.method == 'POST':
        form = EditUserForm(request.form)
        if form.validate():
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            
            # Execute
            cur.execute(
                'UPDATE users SET name=%s, email=%s, phone=%s WHERE id=%s', (name, email, phone, id))
            
            # Commit to DB and Close connection
            current_app.db.connection.commit()
            cur.close()
            
            flash('Usuário atualizado', 'success')
            
            return redirect(url_for('users.users'))
    
    return render_template('users/edit_user.html', form=form)


# Delete users
@bp_users.route('/painel-admin/users/delete_user/<string:id>', methods= ['POST'])
@is_logged_in # Check if the user is logged in
@is_admin_in
def delete_user(id):
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Execute
    cur.execute('DELETE FROM users WHERE id = %s', [id])
    
    # Commit to DB and Close connection
    current_app.db.connection.commit()
    cur.close()
    
    flash('Usuário deletado', 'success')

    return redirect(url_for('users.users'))

# Change user status
@bp_users.route('/painel-admin/users/status_user/<string:id>/<string:status>', methods=['POST'])
@is_logged_in # Check if the user is logged in
@is_admin_in
def status_user(id, status):
    status = status == 'True'
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Execute
    cur.execute('UPDATE users SET is_approved = %s WHERE id = %s', (status, id))
    
    # Commit to DB and Close connection
    current_app.db.connection.commit()
    cur.close()
    
    flash('Status do usuário atualizado', 'success')

    return redirect(url_for('users.users'))

