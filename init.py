import mysql.connector as mq

connection_dict = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root",
    "database": "GreenScape",
    "auth_plugin": "mysql_native_password",
}

if __name__ == "__main__":
    connection = mq.connect(**connection_dict)
    cursor = connection.cursor()
    with open("init.sql", "r") as sql_file:
        cursor.execute(sql_file.read())
