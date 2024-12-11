from flask import Blueprint, render_template, current_app, request
from reports.model_route import check_report_exists, create_new_report, get_report_data
from decorator.access import group_required
from os.path import dirname, join as pathjoin
import json
blueprint_report = Blueprint('report_bp', __name__, template_folder='templates')


@blueprint_report.route('/')
@group_required
def report_menu():
    cur_dir = dirname(dirname(__file__))

    with open(pathjoin(cur_dir, "data/reports.json")) as f:
        reports = json.load(f)
    return render_template('reports_menu.html', reports=reports)


@blueprint_report.route('/create', methods=['GET', 'POST'])
@group_required
def create_report():
    report_name = request.args.get('name')
    if request.method == 'GET':
        return render_template(f"create_{report_name}_report.html")
    
    # POST: обработка данных формы
    try:
        year, month = map(int, request.form.get('year_month').split('-'))
    except ValueError:
        return render_template("report_status.html", status_title='Ошибка ввода данных.', status_msg='Укажите корректный год и месяц.', report_name=report_name)
    # Проверка существования отчета
    exist_info = check_report_exists(current_app.config['db_config'], year, month, report_name)
    if exist_info.status:
        return render_template("report_status.html", status_title='Отчёт уже существует', status_msg=exist_info.error_message, report_name=report_name)
    
    # Создание отчета
    res_info = create_new_report(current_app.config['db_config'], year, month, report_name)
    if res_info.status:
        return render_template("report_status.html", status_title='Отчёт успешно создан.', report_name=report_name)
    return render_template("report_status.html", status_title='Ошибка создания отчёта.', status_msg=res_info.error_message, report_name=report_name)


@blueprint_report.route('/view', methods=['GET', 'POST'])
@group_required
def view_report():
    report_name = request.args.get('name')
    if request.method == 'GET':
        return render_template(f"get_{report_name}_report.html")
    
    # POST: получение данных отчета
    try:
        year, month = map(int, request.form.get('year_month').split('-'))
    except ValueError:
        return render_template("report_status.html", status_title='Ошибка ввода данных.', status_msg='Укажите корректный год и месяц.', report_name=report_name)
    
    # Проверка существования отчета
    exist_info = check_report_exists(current_app.config['db_config'], year, month, report_name)
    if not exist_info.status:
        return render_template("report_status.html", status_title='Отчёт не найден.', status_msg=exist_info.error_message, report_name=report_name)
    
    # Получение данных отчета
    res_info = get_report_data(current_app.config['db_config'], year, month, report_name)
    if not res_info.status:
        return render_template("report_status.html", status_title='Ошибка загрузки отчёта.', status_msg=res_info.error_message, report_name=report_name)
    
    rows, schema = res_info.result
    if not rows:
        return render_template("report_status.html", status_title='Данные отчёта отсутствуют.', report_name=report_name)
    
    return render_template("dynamic_report.html", table_title=f'Отчёт за {year}-{month}', header=schema, rows=rows)