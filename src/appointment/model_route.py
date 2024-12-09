from dataclasses import dataclass
from database.select import select_dict
from datetime import date
from database.insert import insert_many
from database.sql_provider import SQLProvider
import os

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@dataclass
class InfoResponse:
    result: tuple
    error_message: str
    status: bool

def model_route_transaction_visit(db_config: dict, basket: dict):
    _sql_list = []
    for key, value in basket.items():
        print(value)
        _sql = provider.get('insert_visit.sql', doctor=value['appointment'].split('|')[3], 
                            appointment_date=value['date'], 
                            appointment_time_start=value['appointment'].split('|')[0], 
                            appointment_time_end=value['appointment'].split('|')[1], 
                            card=value['patient'].split('|')[0])
        print(_sql)
        _sql_list.append(_sql)
    result = insert_many(db_config, _sql_list)
    return InfoResponse(result, error_message="", status=True)

def get_patient(db_config):
    error_message = ''
    _sql = provider.get('get_patient.sql')
    result = select_dict(db_config, _sql)
    if result:
        return InfoResponse(result=result, error_message=error_message, status=True)
    else:
        return InfoResponse(result=(), error_message="No result", status=False) 

def get_specialization(db_config):
    error_message = ''
    _sql = provider.get('get_specialization.sql')
    result = select_dict(db_config, _sql)
    if result:
        return InfoResponse(result=result, error_message=error_message, status=True)
    else:
        return InfoResponse(result=(), error_message="No result", status=False) 

def get_time(db_config, specialization, date):
    error_message = ''
    _sql = provider.get('get_appointment.sql', specialization=specialization, date=date)
    print(_sql)
    result = select_dict(db_config, _sql)
    print(result)
    if result:
        return InfoResponse(result=result, error_message=error_message, status=True)
    else:
        return InfoResponse(result=(), error_message="No result", status=False) 
