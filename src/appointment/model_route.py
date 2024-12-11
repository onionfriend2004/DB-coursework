from dataclasses import dataclass
from database.select import select_dict
from database.insert import insert, update
from database.sql_provider import SQLProvider
from database.DBcm import DBContextManager
import os

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@dataclass
class InfoResponse:
    result: tuple
    error_message: str
    status: bool

def transaction_visit(db_config: dict, basket: dict):
    try:
        with DBContextManager(db_config) as cursor:
            for key, value in basket.items():
                appointment = value['appointment']
                patient = value['patient']
                _sql = provider.get('insert_visit.sql', doctor=appointment['doctor_id'],
                        appointment_date=value['date'],
                        appointment_time_start=appointment['time_start'],
                        appointment_time_end=appointment['time_end'],
                        card=patient['patient_id'])
                insert(db_config, _sql, cursor)
                _sql = provider.get('update_schedule.sql', doctor=appointment['doctor_id'],
                        appointment_date=value['date'],
                        appointment_time_start=appointment['time_start'],
                        appointment_time_end=appointment['time_end'])
                update(db_config, _sql, cursor)
        return InfoResponse(tuple(), error_message="", status=True)
    except Exception as e:
        return InfoResponse(tuple(), error_message=f"Произошла непредвиденная ошибка: {e}",
                                    status=False)

def get_patient(db_config):
    _sql = provider.get('get_patient.sql')
    result = select_dict(db_config, _sql)
    if result:
        return InfoResponse(result=result, error_message='', status=True)
    else:
        return InfoResponse(result=(), error_message="No result", status=False)

def get_specialization(db_config):
    _sql = provider.get('get_specialization.sql')
    result = select_dict(db_config, _sql)
    if result:
        return InfoResponse(result=result, error_message='', status=True)
    else:
        return InfoResponse(result=(), error_message="No result", status=False)

def get_time(db_config, specialization, date):
    _sql = provider.get('get_appointment.sql', specialization=specialization, date=date)
    result = select_dict(db_config, _sql)
    if result:
        return InfoResponse(result=result, error_message='', status=True)
    else:
        return InfoResponse(result=(), error_message="No result", status=False)
