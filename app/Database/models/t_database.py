from env import DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD
import pyodbc

class Database:
    __connection = None

    @classmethod
    def connect(cls):
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={DB_SERVER};"
            f"DATABASE={DB_NAME};"
            f"UID={DB_USER};"
            f"PWD={DB_PASSWORD};"
        )

        if cls.__connection is None:
            cls.__connection = pyodbc.connect(conn_str)


        try:
            cls.__connection.cursor()
        except pyodbc.ProgrammingError:
            cls.__connection = pyodbc.connect(conn_str)

        return cls.__connection

    @classmethod
    def cursor(cls):
        return cls.connect().cursor()

    @classmethod
    def close_connection(cls):
        if cls.__connection:
            cls.__connection.close()
            cls.__connection = None


if __name__ == "__main__":

    try:
        conn = Database.connect()
        print("Connection Object: ", conn)
        print("Connected Successfully")
    except Exception as e:
        print("Connection failed", e)
