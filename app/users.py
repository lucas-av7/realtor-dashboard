from flask import Blueprint, current_app, request, flash, render_template, redirect, url_for, session
from decorators import is_logged_in, is_admin_in, allow_users
from passlib.hash import sha256_crypt
from form_class import RegisterForm, EditUserForm, PermissionsForm


bp_users = Blueprint('users', __name__)

# User register
@bp_users.route('/painel-admin/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        password = sha256_crypt.hash(str(form.password.data))
        is_admin = False
        is_approved = False
        role = form.role.data

        # Create cursor
        cur = current_app.db.connection.cursor()

        cur.execute('SELECT * FROM users WHERE email = %s', [email])
        duplicate = cur.fetchone()
        if duplicate:
            flash(
                'Este e-mail já está em uso, utilize outro e-mail ou faça login.', 'danger')
            return render_template('users/register.html', form=form)
        else:
            cur.execute('SELECT auto_active_user FROM store')
            is_approved = cur.fetchone()['auto_active_user']

            cur.execute('INSERT INTO users(name, email, phone, password, is_admin, is_approved, role, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())',
                        (name, email, phone, password, is_admin, is_approved, role))

            # Commit to DB and Close connection
            current_app.db.connection.commit()
            cur.close()

            if is_approved:
                flash('Você se cadastrou com sucesso, faça o login.', 'success')
            else:
                flash(
                    'Você se cadastrou com sucesso. Aguarde a aprovação do administrador.', 'success')
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
            is_approved = data['is_approved']
            role = data['role']

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
                else:
                    cur.execute('SELECT * FROM roles WHERE id = %s', [role])
                    permissions = cur.fetchone()
                    session['activate'] = permissions['activate']
                    session['all_products'] = permissions['all_products']
                    session['categories'] = permissions['categories']
                    session['purposes'] = permissions['purposes']
                    session['users'] = permissions['users']
                    session['store'] = permissions['store']

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
@is_logged_in  # Check if the user is logged in
def logout():
    session.clear()
    flash('Você saiu com sucesso', 'success')
    return redirect(url_for('users.login'))


# List users
@bp_users.route('/painel-admin/users')
@is_logged_in  # Check if the user is logged in
@allow_users
def users():
    # Create cursor
    cur = current_app.db.connection.cursor()
    
    user_id = session['user_id']

    result = cur.execute(
        'SELECT users.id as id, name, is_approved, roles.title as role, phone, email FROM users INNER JOIN roles ON users.role=roles.id WHERE is_admin = False AND users.id != %s ORDER BY users.name ASC', [user_id])
    users = cur.fetchall()
    
    for user in users:
        qty_active = cur.execute(
            'SELECT * FROM products WHERE created_by=%s and is_active=True', [user['id']])
        user['qty_active'] = qty_active

        qty_pending = cur.execute(
            'SELECT * FROM products WHERE created_by=%s and is_active=False', [user['id']])
        user['qty_pending'] = qty_pending

    if result > 0:
        return render_template('users/users.html', users=users)
    else:
        error = 'Sem usuários cadastrados.'
        return render_template('users/users.html', error=error)

    # Close connection
    cur.close()


# Edit users
@bp_users.route('/painel-admin/users/edit_user/<string:id>', methods=['GET', 'POST'])
@is_logged_in  # Check if the user is logged in
@allow_users
def edit_user(id):
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Get user by ID
    cur.execute('SELECT * FROM users WHERE id=%s', [id])
    user = cur.fetchone()

    # Get form
    form = EditUserForm(request.form)
    
    # Get Roles
    cur.execute('SELECT * FROM roles ORDER BY title ASC')

    roles = cur.fetchall()
    form.role.choices = [(c['id'], c['title']) for c in roles]

    # Populate title field
    form.name.data = user['name']
    form.email.data = user['email']
    form.phone.data = user['phone']
    form.role.data = user['role']

    if request.method == 'POST':
        form = EditUserForm(request.form)
        form.role.choices = [(c['id'], c['title']) for c in roles]
        if form.validate():
            name = request.form['name']
            email = request.form['email']
            phone = request.form['phone']
            role = request.form['role']

            # Execute
            cur.execute(
                'UPDATE users SET name=%s, email=%s, phone=%s, role=%s WHERE id=%s', (name, email, phone, role, id))

            # Commit to DB and Close connection
            current_app.db.connection.commit()
            cur.close()

            flash('Usuário atualizado', 'success')

            return redirect(url_for('users.users'))

    return render_template('users/edit_user.html', form=form)


# Delete users
@bp_users.route('/painel-admin/users/delete_user/<string:id>', methods=['POST'])
@is_logged_in  # Check if the user is logged in
@allow_users
def delete_user(id):
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Move the products to admin
    cur.execute('SELECT id FROM users WHERE is_admin=True')
    admin_id = cur.fetchone()['id']
    cur.execute('UPDATE products SET created_by=%s WHERE created_by=%s', (admin_id, id))

    # Execute
    cur.execute('DELETE FROM users WHERE id = %s', [id])

    # Commit to DB and Close connection
    current_app.db.connection.commit()
    cur.close()

    flash('Usuário deletado', 'success')

    return redirect(url_for('users.users'))


# Change user status
@bp_users.route('/painel-admin/users/status_user/<string:id>/<string:status>', methods=['POST'])
@is_logged_in  # Check if the user is logged in
@allow_users
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


# Users roles
@bp_users.route('/painel-admin/users/roles', methods=['GET'])
@is_logged_in  # Check if the user is logged in
@is_admin_in
def users_roles():
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Get user by ID
    cur.execute('SELECT * FROM roles ORDER BY title ASC')
    roles = cur.fetchall()

    cur.close()

    return render_template('users/roles.html', roles=roles)


# Create role
@bp_users.route('/painel-admin/users/roles/create', methods=['GET', 'POST'])
@is_logged_in  # Check if the user is logged in
@is_admin_in
def users_roles_create():
    # Get form
    form = PermissionsForm(request.form)

    # Create cursor
    cur = current_app.db.connection.cursor()

    if request.method == 'POST' and form.validate():
        title = form.title.data
        activate = form.activate.data
        all_products = form.all_products.data
        categories = form.categories.data
        purposes = form.purposes.data
        users = form.users.data
        store = form.store.data

        cur.execute('INSERT INTO roles(title, activate, all_products, categories, purposes, users, store) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (title, activate, all_products, categories, purposes, users, store))

        # Commit to DB and Close connection
        current_app.db.connection.commit()
        cur.close()

        flash('Você cadastrou a função com sucesso', 'success')
        return redirect(url_for('users.users_roles'))

    return render_template('users/add_role.html', form=form)


# Edit role
@bp_users.route('/painel-admin/users/roles/edit_role/<string:id>', methods=['GET', 'POST'])
@is_logged_in
@is_admin_in
def edit_role(id):
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Get role by ID
    cur.execute('SELECT * FROM roles WHERE id=%s', [id])
    role = cur.fetchone()

    # Get form
    form = PermissionsForm(request.form)

    # Populate role fields
    form.title.data = role['title']
    form.activate.data = bool(role['activate'])
    form.all_products.data = bool(role['all_products'])
    form.categories.data = bool(role['categories'])
    form.purposes.data = bool(role['purposes'])
    form.users.data = bool(role['users'])
    form.store.data = bool(role['store'])

    if request.method == 'POST':
        form = PermissionsForm(request.form)

        title = form.title.data
        activate = form.activate.data
        all_products = form.all_products.data
        categories = form.categories.data
        purposes = form.purposes.data
        users = form.users.data
        store = form.store.data

        # Execute
        cur.execute('UPDATE roles SET title=%s, activate=%s, all_products=%s, categories=%s, purposes=%s, users=%s, store=%s WHERE id=%s',
                    (title, activate, all_products, categories, purposes, users, store, id))

        # Commit to DB and Close connection
        current_app.db.connection.commit()
        cur.close()

        flash('Permissões atualizadas', 'success')

        return redirect(url_for('users.users_roles'))

    return render_template('users/edit_role.html', form=form)


# Delete role
@bp_users.route('/painel-admin/users/delete_role/<string:id>', methods=['POST'])
@is_logged_in
@is_admin_in
def delete_role(id):
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Execute
    cur.execute('DELETE FROM roles WHERE id = %s', [id])

    # Commit to DB and Close connection
    current_app.db.connection.commit()
    cur.close()

    flash('Função deletada', 'success')

    return redirect(url_for('users.users_roles'))
