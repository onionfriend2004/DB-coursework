from database.DBcm import DBContextManager
class CursorError(Exception):
    pass

def insert(db_config: dict, _sql: str, curs=None):
    if curs:
        result = curs.execute(_sql)
        return result
    #else:
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise CursorError("Cursor could not be created")
        else:
            result = cursor.execute(_sql)

            return result
        
    return False


def update(db_config: dict, _sql: str, curs=None):
    if curs:
        curs.execute(_sql)
    else:
        with DBContextManager(db_config) as cursor:
            if cursor is None:
                raise ValueError("Cursor not created")
            else:
                cursor.execute(_sql)
    return True, 'success'