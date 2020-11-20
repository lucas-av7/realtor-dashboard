from flask import Blueprint, current_app, request, flash, render_template, redirect, url_for
from decorators import is_logged_in, is_admin_in
from form_class import PurposeForm

bp_purposes = Blueprint('purposes', __name__)

# purposes


@bp_purposes.route('/painel-admin/purposes')
@is_logged_in  # Check if the user is logged in
@is_admin_in  # Check if the user is admin
def purposes():
    # Create cursor
    cur = current_app.db.connection.cursor()

    result = cur.execute('SELECT * FROM purposes ORDER BY title ASC')
    purposes = cur.fetchall()

    if result > 0:
        return render_template('purposes/purposes.html', purposes=purposes)
    else:
        error = 'Sem propósitos cadastradas.'
        return render_template('purposes/purposes.html', error=error)

    # Close connection
    cur.close()


# Create purpose
@bp_purposes.route('/painel-admin/purposes/add_purpose', methods=['GET', 'POST'])
@is_logged_in
@is_admin_in
def add_purpose():
    form = PurposeForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        print(title)
        # Create cursor
        cur = current_app.db.connection.cursor()

        cur.execute('SELECT * FROM purposes WHERE title = %s', [title])
        duplicate = cur.fetchone()
        if duplicate:
            flash('Este propósito já existe.', 'danger')
            return render_template('purposes/add_purpose.html', form=form)
        else:
            cur.execute('INSERT INTO purposes(title) VALUES (%s)', [title])

            # Commit to DB and Close connection
            current_app.db.connection.commit()
            cur.close()

            flash('Propósito cadastrado com sucesso.', 'success')
            return redirect(url_for('purposes.purposes'))

    return render_template('purposes/add_purpose.html', form=form)


# Edit purpose
@bp_purposes.route('/painel-admin/purposes/edit_purpose/<string:id>', methods=['GET', 'POST'])
@is_logged_in
@is_admin_in
def edit_purpose(id):
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Get purpose by ID
    cur.execute('SELECT * FROM purposes WHERE id=%s', [id])
    purpose = cur.fetchone()

    # Get form
    form = PurposeForm(request.form)

    # Populate title field
    form.title.data = purpose['title']

    if request.method == 'POST' and form.validate():
        title = request.form['title']

        # Execute
        cur.execute('UPDATE purposes SET title=%s WHERE id=%s', (title, id))

        # Commit to DB and Close connection
        current_app.db.connection.commit()
        cur.close()

        flash('Propósito atualizado', 'success')

        return redirect(url_for('purposes.purposes'))

    return render_template('purposes/edit_purpose.html', form=form)


# Delete purpose
@bp_purposes.route('/painel-admin/purposes/delete_purpose/<string:id>', methods=['POST'])
@is_logged_in
@is_admin_in
def delete_purpose(id):
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Execute
    cur.execute('DELETE FROM purposes WHERE id = %s', [id])

    # Commit to DB and Close connection
    current_app.db.connection.commit()
    cur.close()

    flash('Propósito deletado', 'success')

    return redirect(url_for('purposes.purposes'))
