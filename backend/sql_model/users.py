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
        row = cur.fetchone()
        return dict(row) if row else None


def get_public_by_id(id_persona):
    """
    Obtiene los datos públicos de un usuario (id, nombre; sin password_hash) por su ID_PERSONA.
    Devuelve None si no existe. La usa GET /users/me.
    Añadido: Ahora también selecciona nº coment, nº ratings y rating promedio.
    """
    with get_connection() as con:
        cur = con.execute("""
        SELECT P.ID_PERSONA, P.NOMBRE_USUARIO,
                (SELECT COUNT(*) FROM COMENTARIOS WHERE ID_PERSONA = P.ID_PERSONA) AS NUM_COMENTARIOS,
                (SELECT COUNT(*) FROM CALIFICACIONES WHERE ID_PERSONA = P.ID_PERSONA) AS NUM_CALIFICACIONES,
                (SELECT ROUND(AVG(CALIFICACION), 2) FROM CALIFICACIONES WHERE ID_PERSONA = P.ID_PERSONA) AS PROMEDIO_CALIFICACIONES
            FROM PERSONAS P
            WHERE P.ID_PERSONA = ?
        """, (id_persona,))
        row = cur.fetchone()
        return dict(row) if row else None

# De momento no añadiré funciones para modificar datos de usuarios. Más adelante decidiré si merece la pena la complejidad.