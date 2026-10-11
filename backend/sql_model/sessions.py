from backend.database import get_connection
 
# Modificador de fecha de SQLite. Esto establece la duración de las sesiones.
DURACION_SESION = "+7 days"
 
 
def create_session(token_hash, id_persona):
    """
    Borra las sesiones caducadas (primer execute), borrando lo que caduca antes de "ahora".
    Guarda una sesión nueva que caduca en DURACION_SESION, que es "ahora" + 7 días.
    Un usuario puede tener tantas sesiones como quiera si las inicia con navegadores diferentes,
    eso es hasta que caducan tras la duración predeterminada.
    """
    with get_connection() as con:
        con.execute("DELETE FROM SESIONES WHERE FECHA_EXPIRACION <= datetime('now')")
        con.execute("""
            INSERT INTO SESIONES (TOKEN_HASH, ID_PERSONA, FECHA_EXPIRACION)
            VALUES (?, ?, datetime('now', ?))
        """, (token_hash, id_persona, DURACION_SESION))
 
 
def get_user_id_by_token(token_hash):
    """
    Busca la sesión (con un hash determinado) que NO haya caducado.
    Devuelve el ID_PERSONA de la sesión o None si no existe o ha caducado.
    """
    with get_connection() as con:
        cur = con.execute("""
            SELECT ID_PERSONA FROM SESIONES
                WHERE TOKEN_HASH = ? AND FECHA_EXPIRACION > datetime('now')
        """, (token_hash,))
        row = cur.fetchone()
        return row["ID_PERSONA"] if row else None
 
 
def delete_session(token_hash):
    """
    Borra una sesión (logout). Si no existe, no hace nada, así que no hay errores.
    """
    with get_connection() as con:
        con.execute("DELETE FROM SESIONES WHERE TOKEN_HASH = ?", (token_hash,))