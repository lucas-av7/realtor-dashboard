from flask import Blueprint, current_app, request, flash, render_template, redirect, url_for
from decorators import is_logged_in, is_admin_in
from form_class import CategoryForm

bp_categories = Blueprint('categories', __name__)

# Categories
@bp_categories.route('/painel-admin/categories')
@is_logged_in # Check if the user is logged in
@is_admin_in # Check if the user is admin
def categories():
    # Create cursor
    cur = current_app.db.connection.cursor()

    result = cur.execute('SELECT * FROM categories ORDER BY title ASC')
    categories = cur.fetchall()
    
    if result > 0:
        return render_template('categories/categories.html', categories=categories)
    else:
        error = 'Sem categorias cadastradas.'
        return render_template('categories/categories.html', error=error)

    # Close connection
    cur.close()
    

# Create category
@bp_categories.route('/painel-admin/categories/add_category', methods=['GET', 'POST'])
@is_logged_in
@is_admin_in
def add_category():
    form = CategoryForm(request.form)
    if request.method == 'POST'and form.validate():
        title = form.title.data
        print(title)
        # Create cursor
        cur = current_app.db.connection.cursor()
        
        cur.execute('SELECT * FROM categories WHERE title = %s', [title])
        duplicate = cur.fetchone()
        if duplicate:
            flash('Esta categoria já existe.', 'danger')
            return render_template('categories/add_category.html', form=form)
        else:
            cur.execute('INSERT INTO categories(title) VALUES (%s)', [title])
            
            # Commit to DB and Close connection
            current_app.db.connection.commit()
            cur.close()
            
            flash('Categoria cadastrada com sucesso.', 'success')
            return redirect(url_for('categories.categories'))

    return render_template('categories/add_category.html', form=form)


# Edit category
@bp_categories.route('/painel-admin/categories/edit_category/<string:id>', methods=['GET', 'POST'])
@is_logged_in
@is_admin_in
def edit_category(id):
    # Create cursor
    cur = current_app.db.connection.cursor()
    
    # Get category by ID
    cur.execute('SELECT * FROM categories WHERE id=%s', [id])
    category = cur.fetchone()
    
    # Get form
    form = CategoryForm(request.form)
    
    # Populate title field
    form.title.data = category['title']
    
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        
        # Execute
        cur.execute('UPDATE categories SET title=%s WHERE id=%s', (title, id))
        
        # Commit to DB and Close connection
        current_app.db.connection.commit()
        cur.close()
        
        flash('Categoria atualizada', 'success')
        
        return redirect(url_for('categories.categories'))

    return render_template('categories/edit_category.html', form=form)


# Delete category
@bp_categories.route('/painel-admin/categories/delete_category/<string:id>', methods=['POST'])
@is_logged_in
@is_admin_in
def delete_category(id):
    # Create cursor
    cur = current_app.db.connection.cursor()
    
    # Set products to default category
    cur.execute('UPDATE products SET category=1 WHERE category=%s', [id])

    # Execute
    cur.execute('DELETE FROM categories WHERE id = %s', [id])
    
    # Commit to DB and Close connection
    current_app.db.connection.commit()
    cur.close()
    
    flash('Categoria deletada', 'success')

    return redirect(url_for('categories.categories'))

