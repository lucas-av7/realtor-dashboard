from flask import Blueprint, current_app, request, flash, render_template, redirect, url_for, session
from decorators import is_logged_in
from form_class import ProductForm

bp_products = Blueprint('products', __name__)

# Products

@bp_products.route('/painel-admin/products')
@is_logged_in  # Check if the user is logged in)
def products():
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Get products
    if 'is_admin' in session:
        result = cur.execute(
            'SELECT products.is_active, products.title, products.id, users.name AS created_by, categories.title as category, products.modality FROM products INNER JOIN users INNER JOIN categories ON products.created_by=users.id AND products.category=categories.id ORDER BY category ASC')  
    else: 
        result = cur.execute(
            'SELECT products.is_active, products.title, products.id, users.name AS created_by, categories.title as category, products.modality FROM products INNER JOIN users INNER JOIN categories ON products.created_by=users.id AND products.category=categories.id WHERE products.created_by=%s ORDER BY category ASC', [session['user_id']])
    products = cur.fetchall()

    if result > 0:
        return render_template('products/products.html', products=products)
    else:
        error = 'Sem imóveis cadastrados.'
        return render_template('products/products.html', error=error)


# Add Product
@ bp_products.route('/painel-admin/products/add_product', methods=['GET', 'POST'])
@ is_logged_in  # Check if the user is logged in)
def add_product():
    # Get form
    form = ProductForm(request.form)

    # Create cursor
    cur = current_app.db.connection.cursor()

    # Get categories
    result = cur.execute('SELECT * FROM categories ORDER BY title ASC')

    if result == 0:
        flash('Sem categorias cadastradas, cadastre uma primeiro.', 'danger')
        return redirect(url_for('categories.categories'))

    categories = cur.fetchall()
    form.category.choices = [(c['id'], c['title']) for c in categories]

    if request.method == 'POST' and form.validate():
        is_active = form.is_active.data
        created_by = session['user_id']
        title = form.title.data
        category = form.category.data
        rooms = form.rooms.data
        bathrooms = form.bathrooms.data
        area = form.area.data
        price = form.price.data
        cond_fare = form.cond_fare.data
        iptu_fare  = form.iptu_fare.data
        modality  = form.modality.data
        street  = form.street.data
        district = form.district.data
        city = form.city.data
        state  = form.state.data
        description = form.description.data

        cur.execute('INSERT INTO products(is_active, created_by, title, category, rooms, bathrooms, area, price, cond_fare, iptu_fare, modality, street, district, city, state, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (is_active, created_by, title, category, rooms, bathrooms, area, price, cond_fare, iptu_fare, modality, street, district, city, state, description))

        # Commit to DB and Close connection
        current_app.db.connection.commit()
        cur.close()

        flash('Você cadastrou o imóvel com sucesso', 'success')
        return redirect(url_for('products.products'))

    return render_template('products/add_product.html', form=form)


# Edit Product
@ bp_products.route('/painel-admin/product/edit_product/<string:id>', methods=['GET', 'POST'])
@ is_logged_in  # Check if the user is logged in)
def edit_product(id):
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Get product by ID
    cur.execute('SELECT * FROM products WHERE id=%s', [id])
    product = cur.fetchone()

    # Get form
    form = ProductForm(request.form)

    # Get Categories
    result = cur.execute('SELECT * FROM categories ORDER BY title ASC')

    if result == 0:
        flash('Sem categorias cadastradas, cadastre uma primeiro.', 'danger')
        return redirect(url_for('categories.categories'))

    categories = cur.fetchall()
    form.category.choices = [(c['id'], c['title']) for c in categories]

    # Populate title field
    form.is_active.data = bool(product['is_active'])
    form.title.data = product['title']
    form.category.data = int(product['category'])
    form.rooms.data = product['rooms']
    form.bathrooms.data = product['bathrooms']
    form.area.data = product['area']
    form.price.data = product['price']
    form.cond_fare.data = product['cond_fare']
    form.iptu_fare.data  = product['iptu_fare']
    form.modality.data  = product['modality']
    form.street.data = product['street']
    form.district.data = product['district']
    form.city.data = product['city']
    form.state.data  = product['state']
    form.description.data = product['description']

    if request.method == 'POST':
        form = ProductForm(request.form)
        # It's needed to set the choices again to make it works
        form.category.choices = [(c['id'], c['title']) for c in categories]
        if form.validate():
            is_active  = form.is_active.data
            title = form.title.data
            category = form.category.data
            rooms = form.rooms.data
            bathrooms = form.bathrooms.data
            area = form.area.data
            price = form.price.data
            cond_fare = form.cond_fare.data
            iptu_fare  = form.iptu_fare.data
            modality  = form.modality.data
            street = form.street.data
            district = form.district.data
            city = form.city.data
            state  = form.state.data
            description = form.description.data

            # Execute
            cur.execute('UPDATE products SET is_active=%s, title=%s, category=%s, rooms=%s, bathrooms=%s, area=%s, price=%s, cond_fare=%s, iptu_fare=%s, modality=%s, street=%s, district=%s, city=%s, state=%s, description=%s WHERE id=%s',
                        (is_active, title, category, rooms, bathrooms, area, price, cond_fare, iptu_fare, modality, street, district, city, state, description, id))

            # Commit to DB and Close connection
            current_app.db.connection.commit()
            cur.close()

            flash('Imóvel atualizado', 'success')

            return redirect(url_for('products.products'))

    return render_template('products/edit_product.html', form=form)


# Delete Product
@ bp_products.route('/painel-admin/product/delete_product/<string:id>', methods=['POST'])
@ is_logged_in
def delete_product(id):
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Execute
    cur.execute('DELETE FROM products WHERE id = %s', [id])

    # Commit to DB and Close connection
    current_app.db.connection.commit()
    cur.close()

    flash('Imóvel deletado', 'success')

    return redirect(url_for('products.products'))
