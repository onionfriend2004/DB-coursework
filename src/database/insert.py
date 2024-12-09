from database.DBcm import DBContextManager
from pymysql.err import OperationalError


def insert_one(db_config: dict, _sql: str):

    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError("Cursor not created")
        else:
            try:
                cursor.execute(_sql)
            except OperationalError as error:
                print("error: ", error)
                return False
            else:
                print("Cursor no errors")

    return True

def insert_many(db_config: dict, _sql: list):

    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError("Cursor not created")
        else:
            try:
                for sqll in _sql:
                    cursor.execute(sqll)
            except OperationalError as error:
                print("error: ", error)
                return False
            else:
                print("Cursor no errors")

    return True