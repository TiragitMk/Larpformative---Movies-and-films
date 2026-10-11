"""
Las responsabilidades de este script son básicamente traducir de cabecera de petición HTTP
a usuario actual de sesión. Hay un flujo de información que lleva desde cabecera hasta ID_PERSONA.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from backend import security
 
# auto_error=False: si falta la cabecera, devuelve None en vez de lanzar su propio error,
# para que seamos nosotros quienes respondamos siempre con un 401, que HTTPBEarer a veces
# puede enviar un 403 donde FastAPI devolvería un 401.
bearer_scheme = HTTPBearer(auto_error=False)

# Depends hace que una función se ejecute antes del endpoint.
# HTTPBearer sabe leer la cabecera "Authorization: Bearer <token>".
# HTTPAuthorizationCredentials es el tipo de objeto que devuelve HTTPBearer.
 
ERROR_401_HEADERS = {"WWW-Authenticate": "Bearer"} # Especifica el tipo de autenticación que espera.
 
 
def get_token(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> str:
    """
    Saca el token de la cabecera Authorization, o lanza 401 "No autenticado" si no viene.

    La idea es que el frontend guarde el token y lo envíe cada vez que se entra.
    Si está caducado, dejará de servir.

    No comprueba si el token es válido; eso lo hace get_current_user.
    Por tanto no devuelve el id de usuario, solo el token, porque logout sólo necesita el token.
    """
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado.",
                            headers=ERROR_401_HEADERS)
    return credentials.credentials
 
 
def get_current_user(token: str = Depends(get_token)) -> int:
    """
    Devuelve el ID_PERSONA del usuario dueño del token, o lanza 401 si el token no es válido o ha caducado.
    Es la única fuente del id_persona en los endpoints protegidos, no debe venir del cuerpo de la petición.
    """
    id_persona = security.get_user_id_from_token(token)
    if id_persona is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o caducado.",
                            headers=ERROR_401_HEADERS)
    return id_persona

# Cuando un endpoint pide Depends(get_current_user), necesita get_token, que necesita bearer_scheme.
# Ejecuta en orden: Lee cabecera, extrae token de la petición,
# lo hashea, busca el token hasheado entre las sesiones, y en cualquier caso
# comprueba que no haya caducado.
# Si todo va bien, devuelve el ID_PERSONA, y si hay error no llega al endpoint.

# Logout borra la sesión del token, así que deja de servir.
# Las sesiones caducadas se borran automáticamente en el login.