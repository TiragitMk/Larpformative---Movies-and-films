import sqlite3
from contextlib import contextmanager
from backend.config import DB_PATH

DB_SCHEMA = """
    CREATE TABLE IF NOT EXISTS PERSONAS (
        ID_PERSONA INTEGER PRIMARY KEY AUTOINCREMENT,
        NOMBRE_USUARIO TEXT NOT NULL UNIQUE,
        PASSWORD_HASH TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS PELICULAS (
        ID_PELICULA TEXT PRIMARY KEY,
        NOMBRE TEXT NOT NULL,
        ANIO INTEGER
    );

    CREATE TABLE IF NOT EXISTS COMENTARIOS (
        ID_COMENTARIO INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_PELICULA TEXT NOT NULL REFERENCES PELICULAS(ID_PELICULA),
        ID_PERSONA INTEGER NOT NULL REFERENCES PERSONAS(ID_PERSONA),
        COMENTARIO TEXT NOT NULL,
        FECHA_CREACION TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS CALIFICACIONES (
        ID_CALIFICACION INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_PELICULA TEXT NOT NULL REFERENCES PELICULAS(ID_PELICULA),
        ID_PERSONA INTEGER NOT NULL REFERENCES PERSONAS(ID_PERSONA),
        CALIFICACION INTEGER NOT NULL CHECK (CALIFICACION BETWEEN 1 AND 5),
        FECHA_CREACION TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (ID_PERSONA, ID_PELICULA)
    );
    """

@contextmanager
def get_connection():
    """
    El decorador de @contextmanager habilita el uso de with con las conexiones en las queries,
    y el with lo que hace es almacenar la conexión de con en la variable a la que se asocia,
    haciendo que si todo sale bien siempre se haga commit, y si sale mal haga rollback.
    Al terminar la consulta o modificación de la base de datos, reanuda esta función y o bien
    cierra la conexión, o hace rollback y luego la cierra.

    Esta función crea una conexión con la base de datos, convierte las filas en lista de filas con nombre,
    ejecuta la conexión con foreign keys (que no están por defecto funcionales en sqlite),
    y hace un try. Si la query da error, se deshace, y pase lo que pase se cierra la conexión.
    
    Esto permite reducir cada query del modelo a básicamente dos línea de código, en lugar
    de repetir todo esto. DRY.
    """
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    try:
        yield con
        con.commit()
    except Exception:
        con.rollback()
        raise
    finally:
        con.close()

def init_database():
    """
    Crea la base de datos con el esquema especificado en la constante de arriba.
    """
    with get_connection() as con:
        con.executescript(DB_SCHEMA)

if __name__ == "__main__":
    init_database()