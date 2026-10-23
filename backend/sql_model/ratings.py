from backend.database import get_connection
from backend.omdb_requests.omdb_requests_services import get_movie_api_data
from backend.sql_model.films import is_film_in_db

def add_rating(id_pelicula, id_persona, rating:int):
    """
    Registra una película si no existe en la base de datos, y crea un rating para el
    usuario y la película. Es único por usuario y película.
    Al terminar devuelve True.
    Mucho ojo porque no almacenamos fechas de modificación (de momento), así que si ya existe
    se modifica pero la fecha de modificación no se guarda.
    Como hace ON CONFLICT, no hace falta un edit_rating.

    id_pelicula: imdb_id
    id_persona: id del usuario en la db.
    rating: int del 1 al 5.
    """
    if not is_film_in_db(id_pelicula):
        movie_data = get_movie_api_data(id_pelicula)
        if movie_data is None:
            return None
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
    return True

def get_all_ratings(id_persona):
    with get_connection() as con:
        cur = con.execute("SELECT ID_PELICULA, CALIFICACION, FECHA_CREACION FROM CALIFICACIONES WHERE ID_PERSONA=?",(id_persona,))
        return [dict(i) for i in cur.fetchall()]

def get_rating(id_persona, id_pelicula):
    """
    Obtiene el rating de un usuario en una película.
    Consulta la combinación de persona-película.
    Corregido bug en cur.fetchone()[0] daba TypeError.
    """
    with get_connection() as con:
        cur = con.execute("SELECT CALIFICACION FROM CALIFICACIONES WHERE ID_PERSONA=? AND ID_PELICULA=?",(id_persona, id_pelicula))
        result = cur.fetchone()
        return result[0] if result else None

def get_average_rating(id_pelicula):
    """
    Muestra el promedio de todos los ratings de una película.
    """
    with get_connection() as con:
        cur = con.execute("""
        SELECT ROUND(AVG(CALIFICACION), 2), COUNT(*)
            FROM CALIFICACIONES
            WHERE ID_PELICULA = ?
        """, (id_pelicula,))
        promedio, total = cur.fetchone()
        return {"average": promedio or 0, "count": total}
    
     # Este código da o el promedio, o 0 si no hay ratings.

    # promedio es None si no tiene calificaciones. [0]:promedio, [1]:rating_count.

def get_user_rating_count(id_persona):
    """
    Número de calificaciones de un usuario. Sirve para paginar su lista.
    Se han creado funciones similares para comentarios y películas.
    """
    with get_connection() as con:
        return con.execute("SELECT COUNT(*) FROM CALIFICACIONES WHERE ID_PERSONA = ?", (id_persona,)).fetchone()[0]

def get_user_ratings_head(id_persona, limit=10, page=1):
    """
    Calificaciones de un usuario, paginadas y con el nombre y año de cada película.
    Ordenadas de la más reciente a la más antigua (DESC).
    """
    with get_connection() as con:
        cur = con.execute("""
        SELECT C.ID_PELICULA, P.NOMBRE AS NOMBRE_PELICULA, P.ANIO, C.CALIFICACION, C.FECHA_CREACION
            FROM CALIFICACIONES C
            JOIN PELICULAS P ON P.ID_PELICULA = C.ID_PELICULA
            WHERE C.ID_PERSONA = ?
            ORDER BY C.FECHA_CREACION DESC, C.ID_CALIFICACION DESC
            LIMIT ? OFFSET ?
        """, (id_persona, limit, (page - 1) * limit))
        return [dict(i) for i in cur.fetchall()]

def del_rating(id_persona, id_pelicula):
    """
    Borra la calificación de un usuario en una película.
    Devuelve True si había calificación y se borró y False si no existía.
    """
    with get_connection() as con:
        cur = con.execute("DELETE FROM CALIFICACIONES WHERE ID_PERSONA = ? AND ID_PELICULA = ?",
                          (id_persona, id_pelicula))
        return cur.rowcount > 0     # rowcount = número de filas afectadas por el DELETE.