import mysql.connector as mq
import pandas as pd

connection = mq.connect(
        host='localhost',
        user='root',
        password='root',
        database='GreenScape'
    )

cursor = connection.cursor()
cursor.execute("SELECT * FROM Usuario LIMIT 5")
rows = cursor.fetchall()
user_table = pd.DataFrame.from_records([row for row in rows])
print(user_table)
