from flask import Blueprint, current_app, request, flash, render_template, redirect, url_for, session
from decorators import is_logged_in
from form_class import EditUserForm, EditPasswordForm
from passlib.hash import sha256_crypt


bp_profile = Blueprint('profile', __name__)

# View profile


@bp_profile.route('/painel-admin/profile', methods=['GET'])
@is_logged_in  # Check if the user is logged in
def profile():
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Get user by ID
    user_id = session['user_id']
    cur.execute('SELECT * FROM users WHERE id=%s', [user_id])
    user = cur.fetchone()

    return render_template('profile/profile.html', user=user)


# Edit profile
@bp_profile.route('/painel-admin/edit_profile', methods=['GET', 'POST'])
@is_logged_in  # Check if the user is logged in
def edit_profile():
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Get user by ID
    user_id = session['user_id']
    cur.execute('SELECT * FROM users WHERE id=%s', [user_id])
    user = cur.fetchone()

    # Get form
    form = EditUserForm()

    # Populate profile fields
    form.name.data = user['name']
    form.phone.data = user['phone']
    form.email.data = user['email']

    if request.method == 'POST':
        form = EditUserForm(request.form)
        if form.validate():
            name = form.name.data
            phone = form.phone.data
            email = form.email.data

            cur.execute('UPDATE users SET name=%s, phone=%s, email=%s WHERE id=%s',
                        (name, phone, email, user_id))

            # Commit to DB and Close connection
            current_app.db.connection.commit()
            cur.close()

            flash('Dados atualizados', 'success')

            return redirect(url_for('profile.profile'))

    return render_template('profile/edit_profile.html', form=form)


# Edit password
@bp_profile.route('/painel-admin/edit_password', methods=['GET', 'POST'])
@is_logged_in  # Check if the user is logged in
def edit_password():
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Get user by ID
    user_id = session['user_id']
    cur.execute('SELECT * FROM users WHERE id=%s', [user_id])
    user = cur.fetchone()

    password = user['password']

    # Get form
    form = EditPasswordForm(request.form)

    if request.method == 'POST' and form.validate():
        password_candidate = form.actual_password.data

        if sha256_crypt.verify(password_candidate, password):

            new_password = sha256_crypt.hash(str(form.new_password.data))

            cur.execute('UPDATE users SET password=%s WHERE id=%s',
                        (new_password, user_id))

            # Commit to DB and Close connection
            current_app.db.connection.commit()
            cur.close()

            flash('Senha alterada', 'success')

            return redirect(url_for('profile.profile'))
        else:
            error = 'Erro: senha atual incorreta.'
            return render_template('profile/edit_password.html', error=error, form=form)

    return render_template('profile/edit_password.html', form=form)
