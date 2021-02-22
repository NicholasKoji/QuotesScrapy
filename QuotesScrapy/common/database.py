import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'koji',
    'password': '123456',
    'host': 'localhost',
    'database': 'quotes'
}


def dbConnect():
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print('连接数据库成功')
        return cnx, cursor
