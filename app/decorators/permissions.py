from flask import session, redirect, url_for, flash
from functools import wraps


def allow_all_products(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_admin' in session or session['all_products']:
            return f(*args, **kwargs)
        else:
            flash('Acesso não autorizado para seu perfil.', 'danger')
            return redirect(url_for('dashboard'))
    return wrap


def allow_categories(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_admin' in session or session['categories']:
            return f(*args, **kwargs)
        else:
            flash('Acesso não autorizado para seu perfil.', 'danger')
            return redirect(url_for('dashboard'))
    return wrap


def allow_purposes(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_admin' in session or session['purposes']:
            return f(*args, **kwargs)
        else:
            flash('Acesso não autorizado para seu perfil.', 'danger')
            return redirect(url_for('dashboard'))
    return wrap


def allow_users(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_admin' in session or session['users']:
            return f(*args, **kwargs)
        else:
            flash('Acesso não autorizado para seu perfil.', 'danger')
            return redirect(url_for('dashboard'))
    return wrap


def allow_store(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'is_admin' in session or session['store']:
            return f(*args, **kwargs)
        else:
            flash('Acesso não autorizado para seu perfil.', 'danger')
            return redirect(url_for('dashboard'))
    return wrap
