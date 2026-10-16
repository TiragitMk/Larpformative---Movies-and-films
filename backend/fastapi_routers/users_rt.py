from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from backend import security
from backend.dependencies import get_current_user, get_token
from backend.sql_model import users as users_db
 
router = APIRouter(prefix="/users", tags=["users"])

class RegisterData(BaseModel):
    """
    Cuerpo JSON del registro. Pydantic valida los campos y FastAPI responde 422 si no cumplen.
    Con BasEModel estamos definiendo la forma del cuerpo.
    FastAPI lee el JSON del cuerpo y comprueba si los parámetros que se definen en clases
    tipo BaseModel se cumplen en la petición. Esto pasa si hay parámetros tipo BaseModel.

    Info como la contraseña tiene que ir en el cuerpo de las peticiones,
    porque los enlaces quedan guardados en el navegador.
    Field permite hacer lo que Query hace en los parámetros de URL.

    El patrón de username sólo permite caracteres normales.
    """
    username: str = Field(min_length=3, max_length=30, pattern=r"^[A-Za-z0-9_.-]+$")
    password: str = Field(min_length=8, max_length=128)
 
 
class LoginData(BaseModel):
    """
    Cuerpo JSON de petición del login. Sin reglas de formato. si las reglas del registro cambian
    en el futuro, los usuarios antiguos deben poder seguir entrando. Solo se limita la longitud.
    """
    username: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=1, max_length=128)
 
 
@router.post("/register")
def register(data: RegisterData):
    """
    Crea un usuario. Devuelve 409 (conflict) si el nombre ya existe.
    No inicia sesión, pues el frontend debe llamar después a /users/login.
    """
    id_persona = security.register(data.username, data.password)
    if id_persona is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El nombre de usuario ya existe.")
    return {"id_persona": id_persona, "username": data.username}
 
 
@router.post("/login")
def login(data: LoginData):
    """
    Comprueba las credenciales de login y devuelve un token de sesión.
    El mensaje de error es el mismo si el usuario no existe o si la contraseña es incorrecta,
    para no revelar qué nombres de usuario están registrados.
    """
    id_persona = security.login(data.username, data.password)
    if id_persona is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario o contraseña incorrectos.")
    token = security.create_session_token(id_persona)
    return {"access_token": token, "token_type": "bearer"}
 
 
@router.post("/logout", tags=["protected"])
def logout(token: str = Depends(get_token)):
    """
    Invalida el token actual. Si el token ya no era válido, no pasa nada.
    El frontend debe borrar además el token de localStorage.
    Usa Depends(get_token) porque lo que necesita para borrar sesión es el token de la sesión,
    no el id del usuario o sus datos públicos, como sí necesita /me.
    """
    security.logout(token)
 
 
@router.get("/me", tags=["protected"])
def me(id_persona: int = Depends(get_current_user)):
    """
    Devuelve los datos públicos del usuario autenticado.
    Sirve al frontend para comprobar si el token guardado sigue siendo válido y mostrar el nombre.
    Como usa Depends, está protegido y lanza la cadena de dependencias.
    """
    usuario = users_db.get_public_by_id(id_persona)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado.")
    return usuario

@router.get("/{id_persona}")
def user_profile(id_persona: int = Path(ge=1)):
    """
    Perfil público de cualquier usuario. Muestra nombre, número de comentarios, número de calificaciones
    y promedio de las calificaciones que ha dado. Las listas se piden aparte y paginadas en
    GET /users/{id_persona}/comments y GET /users/{id_persona}/ratings.
    """
    usuario = users_db.get_public_by_id(id_persona)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return usuario