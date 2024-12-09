from flask import Blueprint, session, redirect, url_for, render_template, current_app, request
from database.sql_provider import SQLProvider
import os
from .model_route import model_route_auth_req
from base64 import b64encode

blueprint_auth = Blueprint('auth_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

def create_basic_auth_token(login, password):
    credentials_b64 = b64encode(f'{login}:{password}'.encode('ascii')).decode('ascii')
    token = f'Basic {credentials_b64}'
    return token

@blueprint_auth.route('/')
def auth_index():
    return render_template('login.html')

@blueprint_auth.route('/', methods=['POST'])
def auth_login():
    login = request.form.get('login')
    password = request.form.get('password')
    user_input_data = {'login': login, 'password': password}
    auth_response = model_route_auth_req(current_app.config['db_config'], user_input_data, provider)
    if auth_response.status:
        user_group = auth_response.result[0][2]
        session['user_group'] = user_group
        session['login'] = login
        return redirect(url_for('main_menu'))
    else:
        return render_template('login.html', error_message=auth_response.error_message)
