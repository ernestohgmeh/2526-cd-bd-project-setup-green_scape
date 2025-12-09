import mysql.connector as mq
import pandas as pd

connection = mq.connect(
        host='localhost',
        port = '3307',
        user='root',
        password='root',
        database='GreenScape',
        auth_plugin='mysql_native_password'
    )

cursor = connection.cursor()
<<<<<<< HEAD

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
def favorite_plants():
    query = """
    Select

    """
    return pd.read_sql(query, connection)

#3-d)
def active_users():
    query = """
    SELECT usu.IDU, usu.Nombre, usu.DireccionParticular,
    MAX(
        CASE
            WHEN rcc.Fecha >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH) OR ctr.Fecha >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            THEN GREATEST(COALESCE(rcc.Fecha, '1223-01-01'), COALESCE(ctr.Fecha, '1223-01-01'))
            ELSE NULL
        END
    ) AS Fecha
    FROM Usuario usu
    LEFT JOIN Reaccionar rcc ON usu.IDU = rcc.IDU
    LEFT JOIN Contribucion ctr ON usu.IDU = ctr.IDU
    GROUP BY usu.IDU
    """
    return pd.read_sql(query, connection)


#3-e)
def most_popular_post():
    query = """
    SELECT pub.*, COUNT(rcc.IDU)
    FROM Publicacion pub
    JOIN Reaccionar rcc ON pub.IDPub = rcc.IDPub
    GROUP BY pub.IDPub
    HAVING COUNT(CASE
                    WHEN rcc.Tipo in ('Me encanta', 'Me gusta', 'Me asombra', 'Me divierte') THEN 1 END) >
            COUNT(CASE
                    WHEN rcc.Tipo in ('Me enoja', 'Me entristece') THEN 1 END)
    """
    return pd.read_sql(query,connection)

#3-f)
def se_me_acabo_el_ingles():
    query = """
    SELECT plt.NombreComun
    FROM Planta plt
    JOIN Contribucion as ctr ON plt.IDProd = ctr.IDProd
    WHERE
    """
    return pd.read_sql(query, connection)


#build for query
def change():
    query = """

    """
    return pd.read_sql(query, connection)
##############################
candela = """SELECT 
    TABLE_NAME as tabla,
    COLUMN_NAME as columna,
    CONSTRAINT_NAME as nombre_constraint,
    CASE 
        WHEN CONSTRAINT_NAME = 'PRIMARY' THEN 'PRIMARY KEY'
        WHEN REFERENCED_TABLE_NAME IS NOT NULL THEN 'FOREIGN KEY'
        ELSE 'OTHER'
    END as tipo_clave,
    REFERENCED_TABLE_NAME as referencia_tabla,
    REFERENCED_COLUMN_NAME as referencia_columna
FROM 
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE 
    TABLE_SCHEMA = 'GreenScape'
ORDER BY 
    TABLE_NAME, ORDINAL_POSITION;"""
#print(pd.read_sql(candela, connection)) #tester
#print(pd.read_sql("Select ctr.Tipo from Reaccionar ctr Group By ctr.Tipo ", connection)) #tester

print(se_me_acabo_el_ingles())
=======
# cursor.execute("SELECT * FROM Usuario LIMIT 5")

query = """
SELECT P.NombreComun, G.IDU FROM Planta as P JOIN Gustar as G ON P.IDProd = G.IDProd;

"""

cursor.execute(query)

rows = cursor.fetchall()
user_table = pd.DataFrame.from_records([row for row in rows])
print(user_table)
>>>>>>> a87bc0e (Adding libraries)
