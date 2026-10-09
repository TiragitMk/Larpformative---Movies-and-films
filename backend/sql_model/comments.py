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
        return cur.lastrowid    # Esta línea es opcional.

def get_all_my_comments(id_persona):
    pass

def get_all_my_comments_film(id_persona, id_pelicula):
    pass

def get_all_comments_film(id_pelicula):
    pass

def get_comment(id_comment):
    pass

def edit_comment(id_comment):
    with get_connection() as con:
        con.execute("UPDATE ")

