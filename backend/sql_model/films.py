from backend.database import get_connection

def is_film_in_db(id_pelicula):
    """
    Comprueba si la película ya está registrada en la db.
    Sirve para no llamar SIEMPRE a la api en backend.sql_model.comments o en backend.sql_model.ratings.
    """
    with get_connection() as con:
        cur = con.execute("SELECT COUNT(ID_PELICULA) FROM PELICULAS WHERE ID_PELICULA=?",(id_pelicula,))
        if cur.fetchone()[0] == 0:
            result = False
        else:
            result = True
    return result

def get_film_count():
    """
    Número de películas registradas en la db. Sirve para paginar las listas del search.
    """
    with get_connection() as con:
        return con.execute("SELECT COUNT(*) FROM PELICULAS").fetchone()[0]

def get_all_films_by_rating_head(orden="DESC", limit=10, page=1):
    """
    Muestra un head de todas las películas, ordenadas por rating.
    Parámetro orden="DESC" -> Mayor a menor rating
    Parámetro orden="ASC" -> Menor a mayor rating
    Se añade subconsulta para el número de comentarios de cada una.
    """
    with get_connection() as con:
        cur = con.execute(f"""
        SELECT P.ID_PELICULA, P.NOMBRE, P.ANIO,
                ROUND(AVG(C.CALIFICACION), 2) AS PROMEDIO,
                COUNT(C.ID_CALIFICACION) AS NUM_CALIFICACIONES
                (SELECT COUNT(*) FROM COMENTARIOS CO WHERE CO.ID_PELICULA = P.ID_PELICULA) AS NUM_COMENTARIOS
            FROM PELICULAS P
            LEFT JOIN CALIFICACIONES C ON C.ID_PELICULA = P.ID_PELICULA
            GROUP BY P.ID_PELICULA
            ORDER BY PROMEDIO {orden} NULLS LAST, P.NOMBRE ASC
            LIMIT ? OFFSET ?
        """, (limit, (page-1) * limit))
        return [dict(i) for i in cur.fetchall()]

def get_all_films_by_year_head(orden="DESC", limit=10, page=1):
    """
    Muestra un head de todas las películas, ordenadas por año de salida.
    Parámetro orden="DESC" -> Más nueva a más antigua
    Parámetro orden="ASC" -> Más antigua a más nueva
    """
    with get_connection() as con:
        cur = con.execute(f"""
        SELECT P.ID_PELICULA, P.NOMBRE, P.ANIO,
                ROUND(AVG(C.CALIFICACION), 2) AS PROMEDIO,
                COUNT(C.ID_CALIFICACION) AS NUM_CALIFICACIONES
                (SELECT COUNT(*) FROM COMENTARIOS CO WHERE CO.ID_PELICULA = P.ID_PELICULA) AS NUM_COMENTARIOS
            FROM PELICULAS P
            LEFT JOIN CALIFICACIONES C ON C.ID_PELICULA = P.ID_PELICULA
            GROUP BY P.ID_PELICULA
            ORDER BY P.ANIO {orden} NULLS LAST, P.NOMBRE ASC
            LIMIT ? OFFSET ?
        """, (limit, (page-1) * limit))
        return [dict(i) for i in cur.fetchall()]