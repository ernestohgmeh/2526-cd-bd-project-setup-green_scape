import mysql.connector as mq
import pandas as pd

connection = mq.connect(
        host='localhost',
        port = '3306',
        user='root',
        password='root',
        database='GreenScape'
    )

cursor = connection.cursor()

# cursor.execute("SELECT * FROM Usuario LIMIT 5")
# rows = cursor.fetchall()
# user_table = pd.DataFrame.from_records([row for row in rows])
# print(user_table)]

#3-a)
def get_all_products():
    return pd.read_sql("SELECT * FROM Producto", connection)
  
#3-b)
def count_reactions_per_publication():
    query = f"""SELECT usu.Nombre ,pub.Texto, Count(*) as Cantidad_de_Reacciones
FROM Reaccionar rcc 
JOIN Publicacion pub ON rcc.IDPub = pub.IDPub
JOIN Usuario usu ON pub.IDU = usu.IDU
GROUP BY rcc.IDPub, pub.Texto, usu.Nombre"""

    return pd.read_sql(query, connection)

#3-c)


print(pd.read_sql("SHOW Tables", connection)) #tester