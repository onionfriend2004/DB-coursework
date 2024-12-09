from dataclasses import dataclass
from database.select import select_line, select_list, call_procedure
from database.sql_provider import SQLProvider
import os

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@dataclass
class InfoResponse:
    result: tuple
    error_message: str
    status: bool


def check_report_exists(db_config, year: int, month: int, report_name: str):
    _sql = provider.get(f'get_{report_name}_report.sql', year=year, month=month)
    dict_ = select_line(db_config, _sql)
    if dict_:
        return InfoResponse((dict_,), error_message='Отчёт для указанных данных уже существует', status=True)
    return InfoResponse((dict_,), error_message='', status=False)


def create_new_report(db_config, year: int, month: int, report_name: str):
    status = call_procedure(db_config, f'create_{report_name}_report', year, month)
    if not status:
        return InfoResponse((), 'Ошибка создания отчёта.', False)
    return InfoResponse((), '', True)

def get_report_data(db_config, year: int, month: int, report_name: str):
    _sql = provider.get(f'get_{report_name}_report.sql', year=year, month=month)
    print("SQL query:", _sql)
    result, schema = select_list(db_config, _sql)
    if not result:
        return InfoResponse((), error_message='Отчёт за указанный период не найден.', status=False)
    return InfoResponse((result, schema), error_message='', status=True)
