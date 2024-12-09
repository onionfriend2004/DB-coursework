from flask import Blueprint, session, redirect, render_template, current_app, request, url_for, make_response
from appointment.model_route import model_route_transaction_visit, get_patient, get_specialization, get_time
from decorator.access import group_required
from database.sql_provider import SQLProvider
from datetime import date
import os
import uuid

blueprint_appointment = Blueprint('appointment_bp', __name__, template_folder='templates')

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_appointment.route('/', methods=['GET'])
@group_required
def basket_index():
    if 'basket' not in session:
        session['basket'] = {str(session['login']): {}}
    current_basket = session.get('basket',{})
    print("basketonload:",session.get('basket',{}))
    current_basket = form_basket(current_basket)
    print(current_basket)
    return render_template('basket_dynamic.html', basket=current_basket)

@blueprint_appointment.route('/', methods=['POST'])
@group_required
def basket_main():
    # Нужно извлечь id официанта:
    login = str(session['login'])

    # Получаем корзину:
    session['basket'] = session.get('basket', {login: {}})
    if login not in session['basket']:
        session['basket'][login] = {}

    current_basket = session['basket'][login]
    print("BASKET=", current_basket)

    if request.form.get('delete'):
        visit_id = request.form.get('visit_id')
        if visit_id in current_basket:
            del current_basket[visit_id]
            session.modified = True

    return redirect(url_for('appointment_bp.basket_index'))


@blueprint_appointment.route('/clear_basket')
@group_required
def clear_basket():
    if session.get('basket',{}):
        session.pop('basket')
    return redirect(url_for('appointment_bp.basket_index'))

@blueprint_appointment.route('/add_to_basket')
@group_required
def add_to_basket():
    login = str(session['login'])
    patient = session.get('patient')
    specialization = session.get('specialization')
    date = session.get('date')
    appointment = session.get('appointment')

    if not patient or not specialization or not date or not appointment:
        return render_template('error.html', error_message="Необходимо выбрать все параметры.")

    visit = {
        'patient': patient,
        'specialization': specialization,
        'date': date,
        'appointment': appointment
    }
    print(visit)
    # Получаем корзину:
    session['basket'] = session.get('basket', {login: {}})
    if login not in session['basket']:
        session['basket'][login] = {}

    # Добавляем visit в корзину
    session['basket'][login][str(uuid.uuid4())] = visit
    session.modified = True

    return redirect(url_for('appointment_bp.basket_index'))

@blueprint_appointment.route('/save_appointment', methods=['POST'])
@group_required
def save_appointment():
    if not session.get('basket',{}):
        return redirect(url_for('appointment_bp.basket_index'))
    if not session.get('login',""):
        return render_template("error.html", message="Вы не авторизованы на сайте, авторизируйтесь для регистрации заказа")
    print("Order success")
    current_basket = session.get('basket', {})
    login = session.get('login',"")
    result = model_route_transaction_visit(current_app.config['db_config'], current_basket[login])
    if result.status:
        clear_basket()
        return render_template("order_finish.html")
    else:
        return render_template("error.html", error_message="Заказ не был создан")
    
def form_basket(visits_info: list[dict]) -> list[dict]:
    login = str(session['login'])
    if 'basket' not in session or login not in session['basket'] or not visits_info:
        return []

    basket = []
    for visit_id, visit_info in session['basket'][login].items():
        visit = {
            'visit_id': visit_id,
            'doctor_name': visit_info['appointment'].split('|')[2],
            'doctor_id': visit_info['appointment'].split('|')[3],
            'appointment_date': visit_info['date'],
            'appointment_time_start': visit_info['appointment'].split('|')[0],
            'appointment_time_end': visit_info['appointment'].split('|')[1],
            'patient_name': visit_info['patient'].split('|')[1],
            'patient_id': visit_info['patient'].split('|')[0],
            'diagnosis': visit_info['specialization'],
        }
        basket.append(visit)
    return basket

@blueprint_appointment.route('/select_patient', methods=['GET', 'POST'])
@group_required
def select_patient():
    if request.method == 'GET':
        patients = get_patient(current_app.config['db_config'])
        if patients.result:
            return render_template('select_patient.html', patients=patients.result, prev_page=url_for('appointment_bp.basket_index'))
        return render_template('error.html', error_message=patients.error_message)
    patient = request.form.get('patient_id')
    print(patient)
    session['patient'] = patient
    return redirect(url_for('appointment_bp.select_specialization'))

@blueprint_appointment.route('/select_specialization', methods=['GET', 'POST'])
@group_required
def select_specialization():
    if request.method == 'GET':
        specialization = get_specialization(current_app.config['db_config'])
        if specialization.result:
            return render_template('select_specialization.html', specialization=specialization.result, prev_page=url_for('appointment_bp.select_patient'))
        return render_template('error.html', error_message=specialization.error_message)
    specialization = request.form.get('specialization')
    session['specialization'] = specialization
    return redirect(url_for('appointment_bp.select_date'))

@blueprint_appointment.route('/select_date', methods=['GET', 'POST'])
@group_required
def select_date():
    if request.method == 'GET':
        today = date.today().isoformat()
        return render_template('select_date.html', today=today, prev_page=url_for('appointment_bp.select_specialization'))
    selected_date = request.form.get('date')
    print(selected_date)
    session['date'] = selected_date
    return redirect(url_for('appointment_bp.select_time'))

@blueprint_appointment.route('/select_time', methods=['GET', 'POST'])
@group_required
def select_time():
    if request.method == 'GET':
        specialization = session.get('specialization')
        print(specialization)
        date = session.get('date')
        print(date)
        if not specialization or not date:
            return render_template('error.html', error_message="Необходимо выбрать специализацию и дату.")
        time = get_time(current_app.config['db_config'], specialization=specialization, date=date)
        if time.result:
            return render_template('select_time.html', result=time.result, prev_page=url_for('appointment_bp.select_date'))
        return render_template('error.html', error_message=time.error_message)
    appointment = request.form.get('appointment')
    session['appointment'] = appointment
    return redirect(url_for('appointment_bp.add_to_basket'))