from asyncio.windows_events import NULL
# from multiprocessing import connection
import mysql.connector
from mysql.connector import Error
import database


def connectDB():
    try:
        global connection
        connection = mysql.connector.connect(host='moivepicker-dev.clgftnbfrrf4.us-east-1.rds.amazonaws.com',
                                            database='moivepicker-dev',
                                            user='admin',
                                            password='password')

    except Error as e:
        print("Error while connecting to MySQL", e)

connectDB()

if connection.is_connected():

            

            # mySql_Create_Table_Query = """INSERT INTO Hulu SELECT * FROM Netflix WHERE Service = 'hulu'; COMMIT;"""
            mySql_Create_Table_Query = """DELETE FROM Netflix WHERE Service = 'hulu'; COMMIT;"""


            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()


            result = cursor.execute(mySql_Create_Table_Query)
            print("Data moved successfully")




def disableConnection():
    if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


disableConnection()
