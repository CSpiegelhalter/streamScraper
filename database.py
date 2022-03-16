from asyncio.windows_events import NULL
# from multiprocessing import connection
import mysql.connector
from mysql.connector import Error

# connection = NULL

def connectDB():
    try:
        global connection
        connection = mysql.connector.connect(host='moivepicker-dev.clgftnbfrrf4.us-east-1.rds.amazonaws.com',
                                            database='moivepicker-dev',
                                            user='admin',
                                            password='password')
        

    except Error as e:
        print("Error while connecting to MySQL", e)

def getConnection(movieArray):
    if connection.is_connected():

            mySql_Insert_Data = """INSERT INTO Netflix (Title, Year, Rating, Maturity, Seasons,  Duration, Summary, Genres, Cast, Thumbnail, Service) 
                           VALUES 
                           (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) """


            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            global cursor
            cursor = connection.cursor()


           

            for i in movieArray:
                data = (i.title, i.year, i.rating, i.maturity, i.seasons, i.duration, i.summary, i.genres, i.cast, i.thumbnail, i.service)
                cursor.execute(mySql_Insert_Data, data)
                connection.commit()
                print("Entered successfully?")


def disableConnection():
    if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")



def murderDB():
    connectDB()
    if connection.is_connected():

            burn_With_Fire = """DROP TABLE IF EXISTS Netflix"""

            mySql_Create_Table_Query = """CREATE TABLE Netflix ( 
                                Id int(11) AUTO_INCREMENT NOT NULL,
                                Title varchar(250) NOT NULL,
                                Thumbnail varchar(250),
                                Year varchar(250) NOT NULL,
                                Rating varchar(250),
                                Maturity varchar(250),
                                Seasons varchar(250),
                                Duration varchar(250),
                                Summary varchar(250) NOT NULL,
                                Genres varchar(250) NOT NULL,
                                Cast varchar(250) NOT NULL,
                                Service varchar(250) NOT NULL,
                                PRIMARY KEY (Id)) """

            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            global cursor
            cursor = connection.cursor()

            kill = cursor.execute(burn_With_Fire)
            print("Killed")
            result = cursor.execute(mySql_Create_Table_Query)
            print("Netflix Table created successfully ")

    disableConnection()

# murderDB()