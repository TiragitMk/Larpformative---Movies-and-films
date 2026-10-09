from backend.db_model.database import get_connection

def create_user(username, password_hash):
    """
    Inserta un usuario en la base de datos.
    cur.lastrowid puede ir dentro del with o fuera, es importante que esté dentro sólo para los fetch de sqlite.
    """
    with get_connection() as con:
        cur = con.execute("INSERT INTO PERSONAS(NOMBRE_USUARIO, PASSWORD_HASH) VALUES(?, ?)", (username, password_hash))
        return cur.lastrowid

def get_by_username(username):
    """
    Obtiene todos los datos de un solo usuario de la base de datos.
    """
    with get_connection() as con:
        cur = con.execute("SELECT * FROM PERSONAS WHERE NOMBRE_USUARIO = ?;", (username,))
        return cur.fetchone()

# De momento no añadiré funciones para modificar datos de usuarios. Más adelante decidiré si merece la pena la complejidad.