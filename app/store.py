from flask import Blueprint, current_app, request, flash, render_template, redirect, url_for, session
from decorators import is_logged_in, allow_store
from passlib.hash import sha256_crypt
from form_class import StoreForm


bp_store = Blueprint('store', __name__)

# Edit store


@bp_store.route('/painel-admin/edit_store', methods=['GET', 'POST'])
@is_logged_in  # Check if the user is logged in)
@allow_store
def edit_store():
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Get category by ID
    cur.execute('SELECT * FROM store')
    store = cur.fetchone()

    # Get form
    form = StoreForm(request.form)

    form.name.data = store['name']
    form.phone.data = store['phone']
    form.email.data = store['email']
    form.street.data = store['street']
    form.district.data = store['district']
    form.house_number.data = store['house_number']
    form.city.data = store['city']
    form.state.data = store['state']
    form.auto_active_user.data = bool(store['auto_active_user'])
    
    if request.method == 'POST':
        form = StoreForm(request.form)
        name = form.name.data
        phone = form.phone.data
        email = form.email.data
        street = form.street.data
        district = form.district.data
        house_number = form.house_number.data
        city = form.city.data
        state = form.state.data
        auto_active_user = form.auto_active_user.data

        cur.execute('UPDATE store SET name=%s, phone=%s, email=%s, street=%s, district=%s, house_number=%s, city=%s, state=%s, auto_active_user=%s WHERE id=%s',
                                    (name, phone, email, street, district, house_number, city, state, auto_active_user, store['id']))

        # Commit to DB and Close connection
        current_app.db.connection.commit()
        cur.close()

        flash('Dados atualizados', 'success')

        return redirect(url_for('dashboard'))

    return render_template('store/edit_store.html', form=form)
