import mysql.connector as mq
import pandas as pd

connection = mq.connect(
        host='localhost',
        port = 3306,
        user='root',
        password='root',
        database='GreenScape',
        auth_plugin='mysql_native_password'
    )

cursor = connection.cursor()

def run_query(query_str, connection):
    return pd.read_sql(query_str, connection)

queries_dict = {
    "a": "SELECT * FROM Producto",
    
    "b": """
SELECT usu.Nombre ,pub.Texto, Count(*) as Cantidad_de_Reacciones
FROM Reaccionar rcc 
JOIN Publicacion pub ON rcc.IDPub = pub.IDPub
JOIN Usuario usu ON pub.IDU = usu.IDU
GROUP BY rcc.IDPub, pub.Texto, usu.Nombre
""",
    
    "c": """
Select gus.IDProd, COUNT(*) AS Likes
FROM Gustar gus
GROUP BY gus.IDProd
""",
    
    "d": """
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
""",
    
    "e": """
SELECT pub.*, COUNT(rcc.IDU)
FROM Publicacion pub
JOIN Reaccionar rcc ON pub.IDPub = rcc.IDPub
GROUP BY pub.IDPub
HAVING COUNT(CASE
                WHEN rcc.Tipo IN ('Me encanta', 'Me gusta', 'Me asombra', 'Me divierte') THEN 1 END) >
        COUNT(CASE
                WHEN rcc.Tipo IN ('Me enoja', 'Me entristece') THEN 1 END)
""",
    
    "f": """
SELECT plt.NombreComun
FROM Planta plt
JOIN Contribucion as ctr ON plt.IDProd = ctr.IDProd
JOIN Contribucion as octr ON octr.IDU = ctr.IDU
WHERE (DATE_FORMAT(ctr.Fecha, '%Y-%m-01') = DATE_ADD(DATE_FORMAT(octr.Fecha, '%Y-%m-01'), INTERVAL 1 MONTH)
OR DATE_FORMAT(octr.Fecha, '%Y-%m-01') = DATE_ADD(DATE_FORMAT(ctr.Fecha, '%Y-%m-01'), INTERVAL 1 MONTH))
AND ctr.IDProd = octr.IDProd
""",
    
    "h": """
SELECT
(CASE
    WHEN  YEAR(CURDATE()) - YEAR(usu.FechaDeNacimiento) < 11 THEN "wtf"
    WHEN YEAR(CURDATE()) - YEAR(usu.FechaDeNacimiento) BETWEEN 11 AND 20 THEN "11-20"
    WHEN YEAR(CURDATE()) - YEAR(usu.FechaDeNacimiento) BETWEEN 21 AND 30 THEN "21-30"
    WHEN YEAR(CURDATE()) - YEAR(usu.FechaDeNacimiento) BETWEEN 31 AND 40 THEN "31-40"
    WHEN YEAR(CURDATE()) - YEAR(usu.FechaDeNacimiento) BETWEEN 41 AND 50 THEN "41-50"
    WHEN YEAR(CURDATE()) - YEAR(usu.FechaDeNacimiento) BETWEEN 51 AND 60 THEN "51-60"
    WHEN YEAR(CURDATE()) - YEAR(usu.FechaDeNacimiento) BETWEEN 61 AND 70 THEN "61-70"
    WHEN YEAR(CURDATE()) - YEAR(usu.FechaDeNacimiento) BETWEEN 71 AND 80 THEN "71-80"
    WHEN YEAR(CURDATE()) - YEAR(usu.FechaDeNacimiento) BETWEEN 81 AND 90 THEN "81-90"
    WHEN YEAR(CURDATE()) - YEAR(usu.FechaDeNacimiento) BETWEEN 91 AND 100 THEN "91-100"
    WHEN YEAR(CURDATE()) - YEAR(usu.FechaDeNacimiento) > 100 THEN "en mis tiempos..."
ELSE "Revisate Eso" 
END) AS Rango_de_Edad,
COUNT(*) AS Cant_de_Usuarios,
(COUNT(*) * 100 / (SELECT COUNT(*) FROM Usuario)) AS por_ciento
FROM Usuario usu
GROUP BY Rango_de_Edad
ORDER BY Rango_de_Edad
""",
    
    "l": """
SELECT
FROM GUSTAR gus
JOIN Usuario usu ON gus.IDU = usu.IDU
JOIN Planta plt ON plt.IDProd = gus.IDProd
"""
}

# Comentar esta parte del codigo a conveniencia
# Ejecuta todas las consultas
for inciso, query_str in queries_dict.items():
    print(f"Inciso: {inciso}")
    print(run_query(query_str, connection))

# Ejecuta una consulta
#print(run_query(queries_dict["a"], connection))