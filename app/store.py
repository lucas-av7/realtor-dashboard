from flask import Blueprint, current_app, request, flash, render_template, redirect, url_for, session
from decorators import is_logged_in
from passlib.hash import sha256_crypt
from form_class import StoreForm


bp_store = Blueprint('store', __name__)

# Edit store
@bp_store.route('/painel-admin/edit_store', methods=['GET', 'POST'])
@is_logged_in # Check if the user is logged in)
def edit_store():
    # Create cursor
    cur = current_app.db.connection.cursor()
    
    # Get category by ID
    result = cur.execute('SELECT * FROM store')
    store = cur.fetchone()
    
    # Get form
    form = StoreForm(request.form)
    
    if result > 0:
        # Populate store fields
        form.name.data = store['name']
        form.phone.data = store['phone']
        form.email.data = store['email']
        form.street.data = store['street']
        form.district.data = store['district']
        form.house_number.data = store['house_number']
        form.city.data = store['city']
        form.state.data = store['state']
    
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        street = request.form['street']
        district = request.form['district']
        house_number = request.form['house_number']
        city = request.form['city']
        state = request.form['state']
        
        # Execute
        if result > 0:
            cur.execute('UPDATE store SET name=%s, phone=%s, email=%s, street=%s, district=%s, house_number=%s, city=%s, state=%s WHERE id=%s', (name, phone, email, street, district, house_number, city, state, store['id']))
        else:
            cur.execute('INSERT INTO store(name, phone, email, street, district, house_number, city, state) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (name, phone, email, street, district, house_number, city, state))
        
        # Commit to DB and Close connection
        current_app.db.connection.commit()
        cur.close()
        
        flash('Dados atualizados', 'success')
        
        return redirect(url_for('dashboard'))

    return render_template('store/edit_store.html', form=form)