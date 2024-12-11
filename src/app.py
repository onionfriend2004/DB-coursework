from flask import Flask, render_template, session, json, redirect, url_for
from auth.auth import check_authorization

app = Flask(__name__)
app.secret_key = 'api_key'

@app.route('/')
def main_menu():
    auth_message, auth_status = check_authorization()
    return render_template('main_menu.html', message=auth_message, auth_status=auth_status)


@app.route('/exit')
def exit_func():
    session.clear()
    return redirect(url_for('main_menu'))


def register_configs(app):
    from os.path import dirname, join as pathjoin
    
    cur_dir = dirname(__file__)

    with open(pathjoin(cur_dir, "data/dbconfig.json")) as f:
        app.config['db_config'] = json.load(f)

    with open(pathjoin(cur_dir, "data/db_access.json")) as f:
        app.config['db_access'] = json.load(f)

def register_blueprints(app):
    from requests.route import blueprint_requests
    from reports.route import blueprint_report
    from auth.route import blueprint_auth
    from appointment.route import blueprint_appointment
    
    app.register_blueprint(blueprint_appointment, url_prefix='/appointment')
    app.register_blueprint(blueprint_report, url_prefix='/reports')
    app.register_blueprint(blueprint_requests, url_prefix='/requests')
    app.register_blueprint(blueprint_auth, url_prefix='/auth')

if __name__ == '__main__':
    register_configs(app)
    register_blueprints(app)
    app.run(host='0.0.0.0', port=5001)
