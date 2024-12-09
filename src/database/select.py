
# функции связанные с выполнением запроса в базу данных

from database.DBcm import DBContextManager
from pymysql.err import OperationalError

class CursorError(Exception):
    pass

def select_list(db_config: dict, _sql: str):
    result = ()
    schema = []
    with DBContextManager(db_config) as cursor:

        if cursor is None:
            raise ValueError("Cursor not created")
        else:
            try:
                cursor.execute(_sql)
                result = cursor.fetchall()
            except OperationalError as error:
                print("error: ", error)
                return result, schema
            else:
                print("Cursor no errors")

            schema = [item[0] for item in cursor.description]

    return result, schema

def select_dict(db_config: dict, _sql: str):
    result, schema = select_list(db_config, _sql)
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    return result_dict


def select_string(db_config: dict, _sql: str):
    result = ()
    schema = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError("Cursor not created")
        else:
            try:
                cursor.execute(_sql)
                result = cursor.fetchall()
                print(result)
            except OperationalError as error:
                print("error: ", error)
                return (result, schema)
            else:
                print("Cursor no errors")

            schema = [item[0] for item in cursor.description]
    return result, schema

def select_dict(db_config: dict, _sql: str):
    result, schema = select_list(db_config, _sql)
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    return result_dict

def select_line(db_config: dict, _sql: str, curs=None):
    print(select_string, _sql)
    if curs:
        curs.execute(_sql)
        result = curs.fetchall()
        if not result:
            return dict()
        result = result[0]

        res_dict = dict([(item[0], result[i]) for i, item in enumerate(curs.description)])
        return res_dict
    with DBContextManager(db_config) as cursor:

        if cursor is None:
            raise CursorError("Cursor could not be created")
        else:
            cursor.execute(_sql)
            result = cursor.fetchall()
            if not result:
                return dict()
            result = result[0]

            res_dict = dict([(item[0], result[i]) for i, item in enumerate(cursor.description)])
            return res_dict

    print('With clause was exited early in select.py/select_line')
    return dict()

    return result, schema

def call_procedure(db_config: dict, procedure_name: str, *args) -> bool:
    with DBContextManager(db_config) as cursor:
        if not cursor:
            raise CursorError("Cursor could not be created")
        else:
            cursor.callproc(procedure_name, (*args, ))
    
    return True
