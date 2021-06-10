import pyodbc
from constants import LOCAL_DB_PATH_OFF, LAN_DB_PATH, LIVE_DB_PATH, LOCAL_DB_PATH_HOME


class ConnectDB:
    def __init__(self):
        pass

    @staticmethod
    def read_data():
        message=""
        try:
            conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + LOCAL_DB_PATH_HOME)
        except Exception as e1:
            message = e1
            try:
                conn = pyodbc.connect('DSN=Contract Management;UID= ;PWD= ')
            except Exception as e2:
                message = e2
        try:
            cursor = conn.cursor()
            result = cursor.execute("SELECT * FROM Contractmanagement")
            records = result.fetchall()
            conn.commit()
            conn.close()
            return True, records

        except Exception as e:
            return False, message


    @staticmethod
    def insert_record(fields, values):
        num = len(fields)
        query = f"INSERT into Contractmanagement ({(','.join(fields))}) VALUES "
        query += "("
        for i in range(num):
            query += f"'{values[i]}'"
            if i != num - 1:
                query += ","
        query += ");"
            
        try:
            conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + LOCAL_DB_PATH_HOME)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            conn.close()
            return True, "Data inserted Successfully"

        except Exception as e:
            return False, e

    @staticmethod
    def update_record(fields, values, key_name, key):
        num = len(fields)
        query = "UPDATE Contractmanagement SET "

        for i in range(num):
            query += f"{fields[i]}='{values[i]}'"
            if i != num - 1:
                query += ","

        query += f" WHERE {key_name}={key};"

        print(query)

        try:
            conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + LOCAL_DB_PATH_HOME)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            conn.close()
            return True, "Data updated Successfully"

        except Exception as e:
            return False, e
