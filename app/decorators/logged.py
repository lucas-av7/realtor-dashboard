from flask import session, redirect, url_for, flash
from functools import wraps


# Check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Acesso não autorizado, faça login primeiro.', 'danger')
            return redirect(url_for('login'))
    return wrap