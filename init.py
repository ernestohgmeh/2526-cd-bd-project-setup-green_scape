import mysql.connector as mq

connection_dict = {
        "host": 'localhost',
        "port":  3306,
        "user": 'root',
        "password": 'root',
        "database": 'GreenScape',
        "auth_plugin": 'mysql_native_password'
        }

if __name__ == "__main__":
    connection = mq.connect(**connection_dict)

    cursor = connection.cursor()

    create_doc_table = """
    CREATE TABLE IF NOT EXISTS DocumentoPlanta (
        IDDocumento INT NOT NULL AUTO_INCREMENT,
        IDProd INT NOT NULL,  
        TipoDocumento VARCHAR(255) NOT NULL,
        NombreArchivo VARCHAR(255) NOT NULL,
        RutaArchivo VARCHAR(500) NOT NULL,
        MimeType VARCHAR(100) NOT NULL DEFAULT 'application/octet-stream',
        Tamano BIGINT DEFAULT 0,
        FechaCreacion DATETIME DEFAULT CURRENT_TIMESTAMP,
        FechaActualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        EsPrincipal BOOLEAN DEFAULT FALSE,
        DocumentoPadre INT NULL,
        PRIMARY KEY (IDDocumento),
        FOREIGN KEY (IDProd) REFERENCES Planta(IDProd) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (DocumentoPadre) REFERENCES DocumentoPlanta(IDDocumento) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT UC_PlantaDocumentoPrincipal UNIQUE (IDProd, EsPrincipal),
        CHECK (EsPrincipal IN (0, 1))
    );
    """

    cursor.execute(create_doc_table)