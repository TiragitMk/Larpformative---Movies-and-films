"""
Este script se encarga de toda la seguridad del programa.
Es el programa que hashea, conoce los tokens antes de ser hashes, y maneja
cuestiones relativas a contraseñas y tokens de sesiones.
"""

import hashlib
import hmac
import os
import secrets
import sqlite3
from backend.sql_model import users
from backend.sql_model import sessions

ALGORITMO = "pbkdf2_sha256"
ITERACIONES = 600_000

# Funciones de usuarios.

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
    """
    Registra un usuario, hasheando su contraseña antes de almacenarla en la db.
    Devuelve el ID_PERSONA del user creado o None si el nombre ya existe.
    """
    try:
        return users.create_user(username, hash_password(password))
    except sqlite3.IntegrityError:
        return None

def login(username, password):
    """
    Comprueba si el usuario existe y si la contraseña cuadra. De lo contrario, no devuelve nada.
    Devuelve el ID_PERSONA de la fila de la db.
    Por sí solo no genera una sesión, simplemente devuelve el ID de la persona.
    La sesión se genera con create_session_token.
    """
    usuario = users.get_by_username(username)
    if usuario is None or not verify_password(password, usuario["PASSWORD_HASH"]):
        usuario = {"ID_PERSONA":None}
    return usuario["ID_PERSONA"]

# Funciones de las sesiones.

def hash_token(token):
    """
    Hashea un token con SHA-256 para guardarlo en la db.
    Así si alguien obtiene la base de datos no puede usar los tokens que hay en ella.
    Aquí basta SHA-256 sin sal ni iteraciones porque el token
    es aleatorio y muy largo: no se puede adivinar por fuerza bruta.
    """
    return hashlib.sha256(token.encode("utf-8")).hexdigest()
 
def create_session_token(id_persona):
    """
    Genera un token aleatorio seguro con secrets, guarda su hash en SESIONES en la db y
    devuelve el token literal. token_hex genera 32 bits aleatorios como 64 caracteres hex.
    El token literal solo existe en la respuesta del login y en el navegador del usuario.
    Así el hash sólo sirve para guardar en la db, que es su propósito principal.
    """
    token = secrets.token_hex(32)
    sessions.create_session(hash_token(token), id_persona)
    return token
 
def get_user_id_from_token(token):
    """
    Devuelve el ID_PERSONA del dueño del token, o None si el token no existe o ha caducado.
    """
    return sessions.get_user_id_by_token(hash_token(token))
 
def logout(token):
    """
    Invalida el token borrando su sesión.
    Borra la entrada de la db.
    """
    sessions.delete_session(hash_token(token))