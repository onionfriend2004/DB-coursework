from dataclasses import dataclass
from database.select import select_list
from database.sql_provider import SQLProvider
import os

@dataclass
class InfoResponse:
    result: tuple
    error_message: str
    status: bool

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

def fetch_doctor_specialization(db_config):
    error_message = ''
    _sql = provider.get('fetch_doctor_specialization.sql')
    result, schema = select_list(db_config, _sql)
    if result:
        return InfoResponse([result[0] for result in result], error_message=error_message, status=True)
    else:
        return InfoResponse(result=(), error_message="No result", status=False) 
    
def get_request_data(db_config, request_name: str, **kwargs):
    _sql = provider.get(f'get_{request_name}.sql', **kwargs)
    result, schema = select_list(db_config, _sql)
    print(_sql)
    if result:
        return InfoResponse((result, schema), error_message='', status=True)
    else:
        return InfoResponse(result=(), error_message="No result", status=False)