
from flask import render_template, Blueprint, current_app, request, url_for
from requests.model_route import fetch_doctor_specialization, get_request_data
from decorator.access import group_required

blueprint_requests = Blueprint('requests_bp', __name__, template_folder='templates')

@blueprint_requests.route('/', methods=['GET'])
@group_required
def request_index():
    return render_template("request_index.html")

@blueprint_requests.route('/new_patients', methods=['GET'])
@group_required
def request_new_patients():
    return render_template("get_new_patients.html")

@blueprint_requests.route('/doctor_specialization', methods=['GET'])
@group_required
def request_doctor_specialization():
    response = fetch_doctor_specialization(current_app.config['db_config'])
    if response.status:
        return render_template("get_doctor_specialization.html", result=response.result)
    else:
        return render_template('error.html', error_message=response.error_message)

@blueprint_requests.route('/doctor_hire_date', methods=['GET'])
@group_required
def request_doctor_hire_date():
    return render_template("get_doctor_hire_date.html")

@blueprint_requests.route('/view/<request_name>', methods=['POST'])
@group_required
def request_view(request_name):
    kwargs = {key: value for key, value in request.form.items() if key != 'request_name'}
    response = get_request_data(current_app.config['db_config'], request_name, **kwargs)
    if response.status:
        result, schema = response.result
        return render_template('dynamic_result.html', table_title='Результаты запроса', header=schema, rows=result, prev_page=url_for(f'requests_bp.request_{request_name}'))
    else:
        return render_template('request_error.html', error_message=response.error_message, prev_page=url_for(f'requests_bp.request_{request_name}'))