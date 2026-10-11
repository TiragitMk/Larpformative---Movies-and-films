from backend.database import get_connection

def create_user(nombre_usuario, password_hash):
    """
    Inserta un usuario en la base de datos.
    cur.lastrowid puede ir dentro del with o fuera, es importante que esté dentro sólo para los fetch de sqlite,
    pero lastrowid no lo requiere porque sólo guarda un número, no el objeto row.
    """
    with get_connection() as con:
        cur = con.execute("INSERT INTO PERSONAS(NOMBRE_USUARIO, PASSWORD_HASH) VALUES(?, ?)", (nombre_usuario, password_hash))
        return cur.lastrowid

def get_by_username(nombre_usuario):
    """
    Obtiene todos los datos de un solo usuario de la base de datos.
    Usa su NOMBRE_USUARIO.
    """
    with get_connection() as con:
        cur = con.execute("SELECT * FROM PERSONAS WHERE NOMBRE_USUARIO = ?;", (nombre_usuario,))
        return dict(cur.fetchone())

# De momento no añadiré funciones para modificar datos de usuarios. Más adelante decidiré si merece la pena la complejidad.