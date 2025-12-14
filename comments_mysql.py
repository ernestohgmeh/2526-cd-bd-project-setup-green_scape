import mysql.connector as mq
import pandas as pd


class MySqlCommentSystem:
    def __init__(self, db_config):
        self.db_config = db_config
        init_query = """
            CREATE TABLE IF NOT EXISTS ComentarRec (
                IDComentario INT NOT NULL AUTO_INCREMENT,
                IDU INT NOT NULL,
                IDPub INT NOT NULL,
                Texto TEXT NOT NULL,
                IDPadre INT NULL,
                FechaCreacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (IDComentario),
                FOREIGN KEY (IDU) REFERENCES Usuario(IDU) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (IDPub) REFERENCES Publicacion(IDPub) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (IDPadre) REFERENCES ComentarRec(IDComentario) ON DELETE CASCADE ON UPDATE CASCADE
            )
            """
        connection = self.get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Comentar")
        result = cursor.fetchall()
        comment_df = pd.DataFrame(result)
        # cursor.execute("DROP TABLE Comentar")
        cursor.execute(init_query)
        for row in comment_df.iterrows():
            user_id, publication_id = row["IDU"], row["IDPub"]
            comment_text = row["Texto"]
            self.add_comment(user_id, publication_id, comment_text)
        del comment_df
        connection.commit()
        cursor.close()
        connection.close()

    def get_db_connection(self):
        return mq.connect(**self.db_config)

    def add_comment(self, user_id, publication_id, comment_text, parent_id=None):
        connection = self.get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO ComentarRec (IDU, IDPub, Texto, IDPadre) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (user_id, publication_id, comment_text, parent_id))

    def get_parent_comment(self, comment_id):
        connection = self.get_db_connection()
        cursor = connection.cursor()
        query = """
            SELECT IDComentario
            FROM Comentar c1
            JOIN Comentar c2 ON c1.IDPadre = c2.IDU
            WHERE IDComentario == %s
            """
        cursor.execute(query, (comment_id,))
        return cursor.fetchone()

    def get_conversation(self, comment_id, conversation={}):
        connection = self.get_db_connection()
        cursor = connection.cursor()
        recursive_query = """
            WITH RECURSIVE ConversacionCompleta AS (
                -- Caso base
                SELECT
                    IDComentario,
                    IDU,
                    IDPub,
                    Texto,
                    IDPadre,
                    FechaCreacion,
                    1 as Nivel,
                    CAST(IDComentario AS CHAR(255)) as RutaJerarquica
                FROM Comentar
                WHERE IDComentario = %s

                UNION ALL

                -- Caso recursivo
                SELECT
                    c.IDComentario,
                    c.IDU,
                    c.IDPub,
                    c.Texto,
                    c.IDPadre,
                    c.FechaCreacion,
                    cc.Nivel + 1,
                    CONCAT(cc.RutaJerarquica, ' -> ', c.IDComentario)
                FROM Comentar c
                INNER JOIN ConversacionCompleta cc ON c.IDPadre = cc.IDComentario
                )
        """
        cursor.execute(recursive_query)
        comment = cursor.fetchone()
        comment = pd.DataFrame(comment)
        parent = self.get_parent_comment(comment_id)


from init import connection_dict as connd

Comments = MySqlCommentSystem(connd)
Comments.add_comment(5, 24, "sample comment", 1)
connection = mq.connect.connect(**connd)
cursor = connection.cursor()
cursor.execute("SELECT * FROM ComentarRec")
