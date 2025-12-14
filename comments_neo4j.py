from neo4j import GraphDatabase
import datetime

class Neo4jCommentSystem:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.next_comment_id = 1
        with self.driver.session() as session:
            result = session.run("""
            MATCH (c:Comentario)
            RETURN MAX(c.id) as max_id
            """)
            record = result.single()
            self.next_comment_id = (record["max_id"] or 0) + 1

    def close(self):
        self.driver.close()
    
    def create_comment(self, user_id, publication_id, text, parent_comment_id=None):
        with self.driver.session() as session:
            query = """
            MATCH (u:Usuario {id: $user_id})
            MATCH (p:Publicacion {id: $publication_id})
            CREATE (c:Comentario {
                id: $comment_id,
                texto: $text,
                fechaCreacion: datetime()
            })
            CREATE (u)-[:ESCRIBIO]->(c)
            CREATE (c)-[:PERTENECE_A]->(p)
            """
            
            params = {
                'user_id': user_id,
                'publication_id': publication_id,
                'text': text,
                'comment_id': self.next_comment_id
            }

            self.next_comment_id += 1
            
            session.run(query, params)
            
            if parent_comment_id:
                response_query = """
                MATCH (hijo:Comentario {id: $child_id})
                MATCH (padre:Comentario {id: $parent_id})
                CREATE (hijo)-[:RESPONDE_A]->(padre)
                """
                session.run(response_query, {
                    'child_id': params['comment_id'],
                    'parent_id': parent_comment_id
                })
    
    def get_full_conversation(self, comment_id):
        with self.driver.session() as session:
            query = """
            MATCH (inicial:Comentario {id: $comment_id})
            OPTIONAL MATCH path = (inicial)<-[:RESPONDE_A*]-(respuestas:Comentario)
            WITH inicial, respuestas, length(path) as nivel
            RETURN 
                inicial.id as id_inicial,
                inicial.texto as texto_inicial,
                [(inicial)<-[:ESCRIBIO]-(autor:Usuario) | autor.nombre][0] as autor_inicial,
                collect({
                    id: respuestas.id,
                    texto: respuestas.texto,
                    nivel: nivel,
                    autor: [(respuestas)<-[:ESCRIBIO]-(autor:Usuario) | autor.nombre][0],
                    fecha: respuestas.fechaCreacion
                }) as todas_respuestas
            ORDER BY nivel
            """
            
            result = session.run(query, {'comment_id': comment_id})
            return result.single()
    
    def get_conversation_tree(self, comment_id):
        with self.driver.session() as session:
            query = """
            MATCH (c:Comentario {id: $comment_id})
            CALL apoc.path.subgraphAll(c, {
                relationshipFilter: "<RESPONDE_A",
                labelFilter: "Comentario",
                maxLevel: 20
            })
            YIELD nodes, relationships
            RETURN 
                [node in nodes | {
                    id: node.id,
                    texto: node.texto,
                    autor: [(node)<-[:ESCRIBIO]-(u:Usuario) | u.nombre][0],
                    fecha: node.fechaCreacion
                }] as conversacion_completa,
                size(nodes) as total_comentarios
            """
            
            result = session.run(query, {'comment_id': comment_id})
            return result.single()