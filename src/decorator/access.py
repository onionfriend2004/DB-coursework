from functools import wraps
from flask import session, request, redirect, url_for, current_app, render_template

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth_bp.auth_index'))
    return wrapper

def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            user_role = session.get('user_group')
            user_request = request.endpoint
            access = current_app.config['db_access']

            if user_role in access:
                allowed_endpoints = access[user_role]
                if any(user_request.startswith(endpoint) for endpoint in allowed_endpoints):
                    return func(*args, **kwargs)

            return render_template('error.html', error_message='У вас нет прав')
        else:
            return redirect(url_for('auth_bp.auth_index'))
    return wrapper
