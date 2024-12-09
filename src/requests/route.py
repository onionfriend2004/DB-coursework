
from flask import render_template, Blueprint, current_app, request, url_for
from requests.model_route import fetch_doctor_specialization, get_request_data
from decorator.access import group_required

blueprint_requests = Blueprint('requests_bp', __name__, template_folder='templates')

@blueprint_requests.route('/', methods=['GET'])
@group_required
def index_requests():
    return render_template("index_requests.html")

@blueprint_requests.route('/new_patients', methods=['GET'])
@group_required
def request_new_patients():
    return render_template("request1.html")

@blueprint_requests.route('/doctor_specialization', methods=['GET'])
@group_required
def request_doctor_specialization():
    response = fetch_doctor_specialization(current_app.config['db_config'])
    if response.status:
        return render_template("request2.html", result=response.result)
    else:
        return render_template('error.html', error_message=response.error_message)

@blueprint_requests.route('/doctor', methods=['GET'])
@group_required
def request_doctor():
    return render_template("request3.html")

@blueprint_requests.route('/doctor_hire_date', methods=['GET'])
@group_required
def request_doctor_hire_date():
    return render_template("request4.html")

@blueprint_requests.route('/view/<request_id>', methods=['POST'])
@group_required
def request_view(request_id):
    kwargs = {key: value for key, value in request.form.items() if key != 'request_id'}
    print(kwargs)
    response = get_request_data(current_app.config['db_config'], request_id, **kwargs)
    result, schema = response.result
    if response.status:
        return render_template('dynamic_result.html', table_title='Результаты запроса', header=schema, rows=result, prev_page=url_for('requests_bp.index_requests'))
    else:
        return render_template('error.html', error_message=response.error_message)