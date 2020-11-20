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
            return redirect(url_for('users.login'))
    return wrap


def is_admin_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_admin' in session:
            return f(*args, **kwargs)
        else:
            flash('Acesso não autorizado para seu perfil.', 'danger')
            return redirect(url_for('dashboard'))
    return wrap
