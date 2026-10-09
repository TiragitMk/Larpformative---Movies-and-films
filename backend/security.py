import hashlib
import hmac
import os
from backend.sql_model import users

ALGORITMO = "pbkdf2_sha256"
ITERACIONES = 600_000

def hash_password(password):
    """
    Genera una sal y hashea password con la sal ITERACIONES veces.
    Las iteraciones se usan para introducir un delay en el proceso y dificultar bruteforcing.
    """
    sal = os.urandom(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), sal, ITERACIONES)
    return f"{ALGORITMO}${ITERACIONES}${sal.hex()}${h.hex()}"

def verify_password(password, guardado):
    """
    Verifica la contraseña comparando hashes en hex, que es lo que se puede guardar en la db.
    Permite no almacenar contraseñas, sino hashes.
    """
    try:
        algoritmo, iteraciones, sal_hex, hash_hex = guardado.split("$")
    except ValueError:
        return False
    if algoritmo != ALGORITMO:
        return False
    h = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(sal_hex), int(iteraciones))
    return hmac.compare_digest(h.hex(), hash_hex)


def register(username, password):
    return users.create_user(username, hash_password(password))

def login(username, password):
    """
    Comprueba si el usuario existe y si la contraseña cuadra. De lo contrario, no devuelve nada.
    Devuelve el ID_PERSONA de la fila de la db.
    Por sí solo no genera una sesión, simplemente devuelve el ID de la persona. Debe terminarse.
    """
    usuario = users.get_by_username(username)
    if usuario is None or not verify_password(password, usuario["PASSWORD_HASH"]):
        usuario = {"ID_PERSONA":None}
    return usuario["ID_PERSONA"]