import mysql.connector as mq

class MySqlCommentSystem
    def __init__(self, db_config):
        self.db_config = db_config
        init_query = """
            CREATE TABLE IF NOT EXISTS Comentar (
                IDComentario INT NOT NULL AUTO_INCREMENT,
                IDU INT NOT NULL,
                IDPub INT NOT NULL,
                Texto TEXT NOT NULL,
                PadreID INT NULL,
                FechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (IDComentario),
                FOREIGN KEY (IDU) REFERENCES Usuario(IDU) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (IDPub) REFERENCES Publicacion(IDPub) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (PadreID) REFERENCES Comentario(IDComentario) ON DELETE CASCADE ON UPDATE CASCADE
            )
            """
        connecion = get_db_connection()
        cursor = connecion.cursor()
        cursor.execute("SELECT * FROM Comentar")
        comment_df = cursor.fetchall()
        comment_df = pd.read_sql(comment_df)
        cursor.execute("DROP TABLE Comentar"); cursor.fetchall()
        cursor.execute(init_query)
        for row in comment_df.rows():
            user_id, publication_id = row["IDU"], row["IDPub"]
            comment_text = row["Texto"]
            self.add_comment(user_id, publication_id, comment_text)
        del comment_df
        conn.commit()
        cursor.close()
        conn.close()

    def get_db_connection(self):
        return mysql.connector.connect(**self.db_config)
    
    def add_comment(user_id, publication_id, comment_text, parent_id = None):
        connecion = get_db_connection()
        cursor = connecion.cursor
        query = """INSERT INTO Comentar (IDU, IDPub, Texto, PadreID) VALUES (%s, %s %s %s)"""
        cursor.execute(query, user_id, publication_id, comment_text, parent_id)
    
    def get_parent_comment()
        pass

    def get_conversation()
        recursive_query = """--
            WITH RECURSIVE ConversacionCompleta AS (    
                SELECT 
                    IDComentario,
                    IDU,
                    IDPub,
                    Comentario,
                    ComentarioPadreID,
                    FechaCreacion,
                    1 as Nivel,
                    CAST(IDComentario AS CHAR(255)) as RutaJerarquica
                FROM Comentario
            WHERE IDComentario = 1  
                
                UNION ALL
                    
                SELECT 
                    c.IDComentario,
                    c.IDU,
                    c.IDPub,
                    c.Comentario,
                    c.ComentarioPadreID,
                    c.FechaCreacion,
                    cc.Nivel + 1,
                    CONCAT(cc.RutaJerarquica, ' -> ', c.IDComentario)
                FROM Comentario c
                INNER JOIN ConversacionCompleta cc ON c.ComentarioPadreID = cc.IDComentario
            )

            SELECT 
                cc.IDComentario,
                u.Nombre as Autor,
                cc.Comentario,
                cc.Nivel,
                cc.FechaCreacion,
                cc.RutaJerarquica,
                CASE 
                    WHEN cc.Nivel = 1 THEN 'Comentario Principal'
                    ELSE CONCAT('Respuesta nivel ', cc.Nivel - 1)
                END as TipoComentario
            FROM ConversacionCompleta cc
            JOIN Usuario u ON cc.IDU = u.IDU
            ORDER BY cc.RutaJerarquica, cc.FechaCreacion;
        """