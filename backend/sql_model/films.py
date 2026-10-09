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
