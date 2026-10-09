from backend.database import get_connection
from backend.omdb_requests.omdb_requests_services import get_movie_api_data
from backend.sql_model.films import is_film_in_db

def add_rating(id_pelicula, id_persona, rating:int):
    """
    Registra una película si no existe en la base de datos, y crea un rating para el
    usuario y la película. Es único por usuario y película.
    Se puede hacer un edit_rating, contemplaré la posibilidad cuando llegue a la parte del frontend.
    Al terminar devuelve el id del comentario.
    Mucho ojo porque no almacenamos fechas de modificación (de momento), así que si ya existe
    se modifica pero la fecha de modificación no se guarda.
    Como hace ON CONFLICT, no hace falta un edit_rating.

    id_pelicula: imdb_id
    id_persona: id del usuario en la db.
    rating: int del 1 al 5.
    """
    if not is_film_in_db(id_pelicula):
        movie_data = get_movie_api_data(id_pelicula)
        with get_connection() as con:
            con.execute("INSERT OR IGNORE INTO PELICULAS (ID_PELICULA, NOMBRE, ANIO) VALUES (?, ?, ?)",
                        (id_pelicula, movie_data["Title"], movie_data["Year"]))
            
    with get_connection() as con:
        con.execute("""
            INSERT INTO CALIFICACIONES (ID_PELICULA, ID_PERSONA, CALIFICACION)
            VALUES (?, ?, ?)
            ON CONFLICT (ID_PERSONA, ID_PELICULA) DO UPDATE SET
                CALIFICACION = excluded.CALIFICACION;
                """, (id_pelicula, id_persona, rating))

def get_all_ratings(id_persona):
    with get_connection() as con:
        cur = con.execute("SELECT ID_PELICULA, CALIFICACION, FECHA_CREACION FROM CALIFICACIONES WHERE ID_PERSONA=?",(id_persona,))
        return cur.fetchall()

def get_rating(id_persona, id_pelicula):
    with get_connection() as con:
        cur = con.execute("SELECT CALIFICACION FROM CALIFICACIONES WHERE ID_PERSONA=? AND ID_PELICULA=?",(id_persona, id_pelicula))
        return cur.fetchone()[0] if True else None