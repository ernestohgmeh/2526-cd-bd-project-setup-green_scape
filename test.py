import mysql.connector as mq
import pandas as pd

connection = mq.connect(
        host='localhost',
        port = 3307,
        user='root',
        password='root',
        database='GreenScape',
        auth_plugin='mysql_native_password'
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
def favorite_plants():
    query = """
    Select gus.IDProd, COUNT(*) AS Likes
    FROM Gustar gus
    GROUP BY gus.IDProd
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
                    WHEN rcc.Tipo IN ('Me encanta', 'Me gusta', 'Me asombra', 'Me divierte') THEN 1 END) >
            COUNT(CASE
                    WHEN rcc.Tipo IN ('Me enoja', 'Me entristece') THEN 1 END)
    """
    return pd.read_sql(query,connection)

#3-f)
def Contribuciones_constantes():#revisar por si acaso
    query = """
    SELECT plt.NombreComun
    FROM Planta plt
    JOIN Contribucion as ctr ON plt.IDProd = ctr.IDProd
    JOIN Contribucion as octr ON octr.IDProd = ctr.IDProd
    WHERE DATE_FORMAT(ctr.Fecha, '%Y-%m-01') = DATE_ADD(DATE_FORMAT(octr.Fecha, '%Y-%m-01'), INTERVAL 1 MONTH)
    OR DATE_FORMAT(octr.Fecha, '%Y-%m-01') = DATE_ADD(DATE_FORMAT(ctr.Fecha, '%Y-%m-01'), INTERVAL 1 MONTH)
    """
    return pd.read_sql(query, connection)

#3-h)
def Distribucion_de_Edades():#no tiene en cuenta los meses, por si cumplio anos o no
    query = """
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
    ELSE "revisate eso" 
    END) AS Rango_de_Edad,
    COUNT(*) AS Cant_de_Usuarios,
    (COUNT(*) * 100 / (SELECT COUNT(*) FROM Usuario)) AS por_ciento
    FROM Usuario usu
    GROUP BY Rango_de_Edad
    ORDER BY Rango_de_Edad
    """
    return pd.read_sql(query, connection)

#3-M)
def asd():#
    query = """
    SELECT con.IDProd
    FROM Compra com
    JOIN Contribucion con ON con.IDProd = com.IDProd
    WHERE con.IDU = @influencer
    UNION
    SELECT com.IDProd
    FROM Compra com
    JOIN Contribucion con ON con.IDProd = com.IDProd
    WHERE com.IDUC = @influencer
    """
    return pd.read_sql(query, connection)

#3-l)
def Compras_Contradictorias(): #no se tiene en cuenta la cantidad de cosas que compro y revisar de todas formas 
    query = """
    SELECT 
    (CASE
        WHEN 
            SUM(CASE WHEN com.IDProd = plt.IDProd AND com.IDProd = gus.IDProd THEN 1 ELSE 0 END) < 
            SUM(CASE WHEN com.IDProd = plt.IDProd AND com.IDProd <> gus.IDProd THEN 1 ELSE 0 END)
        THEN usu.IDU
    END) as Raritos
    FROM Usuario usu
    JOIN Gustar gus ON gus.IDU = usu.IDU
    JOIN Compra com ON com.IDUC = usu.IDU
    JOIN Planta plt ON plt.IDProd = com.IDProd
    GROUP BY usu.IDU
    ORDER BY usu.IDU
    """
    return pd.read_sql(query, connection)

#3-p)
def Analisis_de_influencers_y_su_impacto_en_ventas():
    query1 = """
    SELECT
    pub.IDU,
    AVG((rcc.peso + com.cant*2)/(rcc.cant + com.cant)) AS Puntaje_de_Interacciones
    FROM Publicacion pub
    LEFT JOIN (
            SELECT rcc.IDPub,
            (COALESCE(SUM(CASE 
                WHEN rcc.Tipo = "Me gusta" THEN 1
                WHEN rcc.Tipo = "Me encanta" THEN 2
                WHEN rcc.Tipo = "Me asombra" THEN 1.5 END), 0)) AS peso,
            COALESCE(SUM(CASE WHEN rcc.Tipo IN ('Me gusta', 'Me encanta', 'Me asombra') THEN 1 END), 0) as cant
            FROM Reaccionar rcc
            GROUP BY rcc.IDPub) rcc ON pub.IDPub = rcc.IDPub
    LEFT JOIN (
        SELECT com.IDPub,
        COALESCE(SUM( CASE WHEN com.Comentario IS NOT NULL THEN 1 ELSE 0 END), 0) AS cant
        FROM Comentar com
        GROUP BY com.IDPub
    ) com ON com.IDPub = pub.IDPub
    GROUP BY pub.IDU
    ORDER BY Puntaje_de_Interacciones DESC
    LIMIT 5
    """
    query2 = """
    SELECT con.IDProd
    FROM Contribucion con
    WHERE con.IDU = @influencer
    UNION
    SELECT com.IDProd
    FROM Compra com
    WHERE com.IDUC = @influencer
    """

    #las subconsultas son el query2, arregla eso si puedes para que sea mas legible
    for_query3 = """
    SELECT com.Fecha
    FROM Compra com
    WHERE com.IDU = @influencer
    AND com.IDProd in (
        SELECT con.IDProd
        FROM Contribucion con
        WHERE con.IDU = @influencer
        UNION
        SELECT com.IDProd
        FROM Compra com
        WHERE com.IDUC = @influencer)
    UNION
    SELECT ctr.Fecha
    FROM Contribucion ctr
    WHERE ctr.IDU = @influencer
    AND ctr.IDProd in (
        SELECT con.IDProd
        FROM Contribucion con
        WHERE con.IDU = @influencer
        UNION
        SELECT com.IDProd
        FROM Compra com
        WHERE com.IDUC = @influencer)
    """
    #for_query3 es para llamarlo para usarlo aqui
    query3 = """
    CREATE TEMPORARY TABLE fechas_acciones AS
    SELECT com.Fecha
    FROM Compra com
    WHERE com.IDU = @influencer
    AND com.IDProd in (
        SELECT con.IDProd
        FROM Contribucion con
        WHERE con.IDU = @influencer
        UNION
        SELECT com.IDProd
        FROM Compra com
        WHERE com.IDUC = @influencer)
    UNION
    SELECT ctr.Fecha
    FROM Contribucion ctr
    WHERE ctr.IDU = @influencer
    AND ctr.IDProd in (
        SELECT con.IDProd
        FROM Contribucion con
        WHERE con.IDU = @influencer
        UNION
        SELECT com.IDProd
        FROM Compra com
        WHERE com.IDUC = @influencer);




    WITH periodos AS (
    SELECT 
        fa.Fecha as fecha_publicacion,
        (
        SELECT COUNT(*)
        FROM Compra com
        WHERE com.Fecha BETWEEN DATE_SUB(fa.Fecha, INTERVAL 14 DAY) AND fa.Fecha
        AND com.IDProd IN (
                    SELECT con.IDProd FROM Contribucion con WHERE con.IDU = @influencer
                    UNION
                    SELECT com.IDProd FROM Compra com WHERE com.IDUC = @influencer)
        ) AS ventas_antes,
        
        (
        SELECT COUNT(*)
        FROM Compra c
        WHERE c.Fecha BETWEEN DATE_ADD(fa.Fecha, INTERVAL 1 DAY) AND DATE_ADD(fa.Fecha, INTERVAL 14 DAY)
        AND c.IDProd IN (
                SELECT con.IDProd FROM Contribucion con WHERE con.IDU = @influencer
                UNION
                SELECT com.IDProd FROM Compra com WHERE com.IDUC = @influencer)
        ) AS ventas_despues
    FROM fechas_acciones fa)
    
    
    SELECT fecha_publicacion, ventas_antes, ventas_despues,
    CASE 
        WHEN ventas_antes = 0 THEN 
            CASE WHEN ventas_despues > 0 THEN 100 ELSE 0 END
        ELSE ((ventas_despues - ventas_antes) * 100 / ventas_antes) END AS incremento_porcentual
    FROM periodos
    """
    query4 = """
    CREATE TEMPORARY TABLE usuarios_reaccionaron AS
    SELECT DISTINCT rcc.IDU, rcc.Fecha
    FROM Reaccionar rcc
    JOIN Publicacion pub ON rcc.IDPub = pub.IDPub
    WHERE pub.IDU = @influencer;

    SELECT  
    COUNT(DISTINCT CASE WHEN EXISTS (
        SELECT 1 
        FROM Compra com
        WHERE com.IDUC = ur.IDU
        AND com.Fecha BETWEEN ur.Fecha AND DATE_ADD(ur.Fecha, INTERVAL 14 DAY)) THEN ur.IDU END) AS usuarios_compraron
    FROM usuarios_reaccionaron ur

    """
    return pd.read_sql(query1, connection)

#build for query
def change():
    query = """

    """
    return pd.read_sql(query, connection)
##############################
#print(pd.read_sql("Select * from Publicacion", connection)) #tester
print(asd())

# cursor.execute("SELECT * FROM Usuario LIMIT 5")

# query = """
# SELECT P.NombreComun, G.IDU FROM Planta as P JOIN Gustar as G ON P.IDProd = G.IDProd;

# """

# cursor.execute(query)

# rows = cursor.fetchall()
# user_table = pd.DataFrame.from_records([row for row in rows])
# print(user_table)