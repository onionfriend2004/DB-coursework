from dataclasses import dataclass
from database.select import select_string

@dataclass
class AuthResponse:
    result: tuple
    error_message: str
    status: bool

def model_route_auth_req(db_config, user_input_data, sql_provider):
    error_message = ''
    _sql = sql_provider.get('check_user.sql', login=user_input_data['login'], password=user_input_data['password'])
    result, schema = select_string(db_config, _sql)
    if result:
        return AuthResponse(result, error_message=error_message, status=True)
    return AuthResponse(result, error_message='неправильный логин или пароль', status=False)
