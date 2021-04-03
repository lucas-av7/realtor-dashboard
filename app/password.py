from flask import Blueprint, current_app, request, flash, render_template, redirect, url_for
from passlib.hash import sha256_crypt
from form_class import EmailForm, PasswordRecoveryForm
from services import sendEmail
import random

bp_password = Blueprint('password', __name__)


# Create recovery code
@bp_password.route('/painel-admin/password/recovery', methods=['GET', 'POST'])
def email_check():
    form = EmailForm(request.form)
    if request.method == 'POST' and form.validate():
        email = request.form['email']
        print(email)

        # Create cursor
        cur = current_app.db.connection.cursor()

        result = cur.execute('SELECT * FROM users WHERE email = %s', [email])
        if result > 0:
            user_id = cur.fetchone()['id']

            # Generate random code
            code = ''
            for x in range(7):
                x = str(random.randrange(10))
                code = code + x

            try:
                subject = 'Código de recuperação de senha'
                body = 'Imobiliária - Use o seguinte código para mudar sua senha: ' + code
                sendEmail(subject, body, email)
                cur.execute(
                    'INSERT INTO pw_recovery(user_id, code) VALUES (%s, %s)', (user_id, code))

                # Commit to DB and Close connection
                current_app.db.connection.commit()
                cur.close()

                flash('Foi enviado um código para o seu e-mail!', 'success')
                return redirect(url_for('password.new_password'))
            except:
                error = 'Erro ao enviar e-mail, tente novamente mais tarde.'
                return render_template('password/email_check.html', error=error)
        else:
            error = 'Email não encontrado no banco de dados.'
            return render_template('password/email_check.html', error=error)

    return render_template('password/email_check.html')


# Change password
@bp_password.route('/painel-admin/password/new_password', methods=['GET', 'POST'])
def new_password():
    form = PasswordRecoveryForm(request.form)
    if request.method == 'POST' and form.validate():
        code = form.code.data
        password = sha256_crypt.hash(str(form.password.data))

        # Create cursor
        cur = current_app.db.connection.cursor()

        result = cur.execute(
            'SELECT * FROM pw_recovery WHERE code = %s', [code])
        if result > 0:
            user_id = cur.fetchone()['user_id']
            cur.execute('UPDATE users SET password=%s WHERE id=%s',
                        [password, user_id])
            cur.execute(
                'DELETE FROM pw_recovery WHERE user_id = %s', [user_id])

            # Commit to DB and Close connection
            current_app.db.connection.commit()
            cur.close()

            flash('Senha alterada com sucesso.', 'success')

            return redirect(url_for('users.login'))
        else:
            error = 'Código de recuperação inválido.'
            return render_template('password/new_password.html', error=error, form=form)

    return render_template('password/new_password.html', form=form)
