import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'koji',
    'password': '123456',
    'host': 'localhost',
    'port': 3306,
    'database': 'quotes'
}


sqlalchemyURL = f'mysql+mysqlconnector://{config["user"]}:{config["password"]}@{config["host"]}:{config["port"]}/{config["database"]}?charset=utf8'


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
        return cnx, cursor

def truncateTable(cnx, cursor, tableName):
    # 使用truncate table删除带有被引用外键的表，需要禁用外键约束
    cursor.execute('set foreign_key_checks=0')
    cursor.execute(f'truncate table {tableName}')
    cursor.execute('set foreign_key_checks=1')
    cursor.execute(f'ALTER TABLE {tableName} AUTO_INCREMENT = 10000')
    cnx.commit()