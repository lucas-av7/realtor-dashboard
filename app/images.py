from flask import Blueprint, current_app, request, flash, render_template, redirect, url_for, session
from decorators import is_logged_in
from services import upload_image
import base64

bp_images = Blueprint('images', __name__)

# Images
@bp_images.route('/painel-admin/product/images/<string:product_id>', methods=['GET', 'POST'])
@is_logged_in # Check if the user is logged in)
def images(product_id):
    # Create cursor
    cur = current_app.db.connection.cursor()
    
    # Get images by product ID
    result = cur.execute('SELECT products.id AS product_id, products.title AS product_title, images.id AS image_id, images.main, images.url, images.url_thumb, images.delete_url FROM products INNER JOIN images ON products.id=images.product_id WHERE product_id=%s ORDER BY images.id ASC', [product_id])
    images = cur.fetchall()
    cur.execute('SELECT title FROM products WHERE id=%s', product_id)
    title = cur.fetchone()['title']
    
    if request.method == 'POST':
        pic = request.files['pic']
        
        if not pic:
            flash('Foto não selecionada corretamente', 'danger')
            return render_template('products/images/images.html', images=images, title=title)
        
        base64img = base64.b64encode(pic.read())
        (url, url_thumb, url_medium, delete_url) = upload_image(base64img)
        
        photos = cur.execute('SELECT * FROM images WHERE product_id=%s and main=True', [product_id])
        main = photos == 0
        
        cur.execute('INSERT INTO images(main, product_id, url, url_thumb, url_medium, delete_url) VALUES (%s, %s, %s, %s, %s, %s)', (main, product_id, url, url_thumb, url_medium, delete_url))
        
        # Commit to DB and Close connection
        current_app.db.connection.commit()
        cur.close()
        
        flash('Imagem adicionada com sucesso', 'success')
        return redirect(url_for('images.images', product_id=product_id))
    
    
    if result > 0:
        return render_template('products/images/images.html', images=images, title=title)
    else:
        error = 'Sem imagens enviadas.'
        return render_template('products/images/images.html', error=error, title=title)
    
    
# Set Main Image
@bp_images.route('/painel-admin/product/images/main/<string:product_id>/<string:image_id>', methods=['POST'])
@is_logged_in # Check if the user is logged in)
def main_image(product_id, image_id):
    # Create cursor
    cur = current_app.db.connection.cursor()
    
    result = cur.execute('SELECT * FROM images WHERE main=True')
    if result > 0:
        old_main_id = cur.fetchone()['id']
        cur.execute('UPDATE images SET main=False WHERE id=%s', [old_main_id])

    cur.execute('UPDATE images SET main=True WHERE id=%s', [image_id])
    
    # Commit to DB and Close connection
    current_app.db.connection.commit()
    cur.close()
    
    flash('Foto principal atualizada', 'success')
    return redirect(url_for('images.images', product_id=product_id))

    
# Delete Image
@bp_images.route('/painel-admin/product/images/delete/<string:product_id>/<string:id>', methods=['POST'])
@is_logged_in # Check if the user is logged in)
def delete_image(product_id, id):
    
    # Create cursor
    cur = current_app.db.connection.cursor()

    # Execute
    cur.execute('DELETE FROM images WHERE id = %s', [id])
    
    # Commit to DB and Close connection
    current_app.db.connection.commit()
    cur.close()
    
    flash('Imagem deletada com sucesso', 'success')
    return redirect(url_for('images.images', product_id=product_id))