"""
Todo esto son comandos relacionados con los comentarios, incluyendo queries relacionadas
con un usuario en específico, película en específico, etc.
Hay funcionalidades para añadir comentarios, obtener información, eliminarlos...
"""

from backend.database import get_connection
from backend.omdb_requests.omdb_requests_services import get_movie_api_data
from backend.sql_model.films import is_film_in_db

def add_comment(id_pelicula, id_persona, comentario:str):
    """
    Registra una película si no existe en la base de datos, y crea un comentario para el
    usuario y la película.
    Se puede hacer un edit_comment, contemplaré la posibilidad cuando llegue a la parte del frontend.
    """
    if not is_film_in_db(id_pelicula):
        movie_data = get_movie_api_data(id_pelicula)
        with get_connection() as con:
            con.execute("INSERT OR IGNORE INTO PELICULAS (ID_PELICULA, NOMBRE, ANIO) VALUES (?, ?, ?)",
                        (id_pelicula, movie_data["Title"], movie_data["Year"]))
            
    with get_connection() as con:
        cur = con.execute("INSERT INTO COMENTARIOS (ID_PELICULA, ID_PERSONA, COMENTARIO) VALUES (?, ?, ?)",
                          (id_pelicula, id_persona, comentario))
        return cur.lastrowid    # Esta línea es opcional. Puede servir para disponer el nuevo comentario.

def get_all_my_comments(id_persona):
    """
    Devuelve TODOS los comentarios de un usuario.
    OJO: Devuelve TODOS los resultados. Más abajo hay uno igual, pero que devuelve los primeros 10.
    """
    with get_connection() as con:
        cur = con.execute("""
        SELECT C.ID_COMENTARIO, C.ID_PELICULA, P.NOMBRE, C.COMENTARIO, C.FECHA_CREACION
            FROM COMENTARIOS C
            JOIN PELICULAS P ON P.ID_PELICULA = C.ID_PELICULA
            WHERE C.ID_PERSONA = ?
            ORDER BY C.FECHA_CREACION DESC
        """, (id_persona,))
        return cur.fetchall()

def get_my_comment_count(id_persona):
    """
    Muestra sólo el número de comentarios (comment count) que tiene un usuario.
    """
    with get_connection() as con:
        cur = con.execute("SELECT COUNT(*) FROM COMENTARIOS WHERE ID_PERSONA = ?", (id_persona,))
        return cur.fetchone()[0]

def get_all_my_comments_film(id_persona, id_pelicula):
    """
    Muestra TODOS los comentarios de una persona en una película.
    OJO: Devuelve TODOS los resultados. Más abajo hay uno igual, pero que devuelve los primeros 10.
    """
    with get_connection() as con:
        cur = con.execute("""
        SELECT ID_COMENTARIO, COMENTARIO, FECHA_CREACION
            FROM COMENTARIOS
            WHERE ID_PERSONA = ? AND ID_PELICULA = ?
            ORDER BY FECHA_CREACION DESC
        """, (id_persona, id_pelicula))
        return cur.fetchall()

def get_all_comments_film(id_pelicula):
    """
    Muestra TODOS los comentarios de una película.
    OJO: Devuelve TODOS los resultados. Más abajo hay uno igual, pero que devuelve los primeros 10.
    """
    with get_connection() as con:
        cur = con.execute("SELECT * FROM COMENTARIOS WHERE ID_PELICULA = ? ORDER BY FECHA_CREACION DESC", (id_pelicula,))
        return cur.fetchall()

def get_film_comment_count(id_pelicula):
    with get_connection() as con:
        cur = con.execute("SELECT COUNT(*) FROM COMENTARIOS WHERE ID_PELICULA = ?", (id_pelicula,))
        return cur.fetchone()[0]

def get_comment(id_comentario):
    """
    Muestra los datos de un comentario específico.
    """
    with get_connection() as con:
        cur = con.execute("SELECT * FROM COMENTARIOS WHERE ID_COMENTARIO = ?", (id_comentario,))
        return cur.fetchone()   # None si no existe

def edit_comment(id_comentario, nuevo_texto):
    """
    Permite editar un comentario, pero sólo el texto.
    """
    with get_connection() as con:
        con.execute("UPDATE COMENTARIOS SET COMENTARIO = ? WHERE ID_COMENTARIO = ?", (nuevo_texto, id_comentario))

def del_comment(id_comentario):
    """
    Permite borrar un comentario con su id.
    """
    with get_connection() as con:
        con.execute("DELETE FROM COMENTARIOS WHERE ID_COMENTARIO = ?", (id_comentario,))

# CONSULTAN SOLO UN HEAD ORDENADO (parámetros default 10 comentarios, página 1):

def get_all_my_comments_head(id_persona, limit=10, page=1):
    """
    Muestra una lista de los primeros limit comentarios de una persona.
    Usa page para paginar la lista.
    Los ordena por fecha de creación o en su defecto ID_COMENTARIO.
    """
    with get_connection() as con:
        cur = con.execute("""
        SELECT * FROM COMENTARIOS
            WHERE ID_PERSONA = ?
            ORDER BY FECHA_CREACION DESC, ID_COMENTARIO DESC
            LIMIT ? OFFSET ?
        """, (id_persona, limit, page * limit))
        return cur.fetchall()

def get_all_my_comments_film_head(id_persona, id_pelicula, limit=10, page=1):
    """
    Muestra una lista de los primeros limit comentarios de un usuario en una película específica,
    usando page para paginar y la combinación id_persona-id_pelicula para indexar los comentarios.
    Los ordena por fecha de creación o ID_COMENTARIO.
    """
    with get_connection() as con:
        cur = con.execute("""
        SELECT * FROM COMENTARIOS
            WHERE ID_PERSONA = ? AND ID_PELICULA = ?
            ORDER BY FECHA_CREACION DESC, ID_COMENTARIO DESC
            LIMIT ? OFFSET ?
        """, (id_persona, id_pelicula, limit, page * limit))
        return cur.fetchall()

def get_all_comments_film(id_pelicula, limit=10, page=1):
    """
    Muestra una lista de los primeros limit comentarios de una película, entre todos los usuarios
    que la han comentado. Usa page para paginar y ordena por fecha de creación o ID_comentario.
    """
    with get_connection() as con:
        cur = con.execute("""
        SELECT * FROM COMENTARIOS
            WHERE ID_PELICULA = ?
            ORDER BY FECHA_CREACION DESC, ID_COMENTARIO DESC
            LIMIT ? OFFSET ?
        """, (id_pelicula, limit, page * limit))
        return cur.fetchall()