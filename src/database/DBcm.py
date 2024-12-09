from pymysql import connect
from pymysql.err import OperationalError

class DBContextManager:
    def __init__(self, db_config: dict):
        self.conn = None
        self.cursor = None
        self.db_config = db_config

    def __enter__(self):
        try:
            self.conn = connect(**self.db_config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except OperationalError as err:
            print(f"OperationalError: {err}")
            return None
        except AttributeError as err:
            print(f"AttributeError: {err}")
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"Exception type: {exc_type}")
        if self.cursor:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.cursor.close()
        if self.conn:
            self.conn.close()
        return True
