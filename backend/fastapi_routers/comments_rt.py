from fastapi import APIRouter, HTTPException, status, Path, Query, Depends
from pydantic import BaseModel, Field, ConfigDict
from backend.sql_model import comments as comments_db
from backend.sql_model import users as users_db
from backend.fastapi_routers.films_rt import IMDB_ID_PATTERN
from backend.dependencies import get_current_user, get_token
 
router = APIRouter(tags=["comments"])
 
class CommentData(BaseModel):
    """
    Recorta espacios antes de validar la longitud.
    """
    model_config = ConfigDict(str_strip_whitespace=True)
    content: str = Field(min_length=1, max_length=400)

@router.get("/comments")
def latest_comments(
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1),
):
    """
    Últimos comentarios de toda la web, con autor y película. Pensado para una sección
    "actividad reciente" en la portada. Puede que no la use según la complejidad
    que le suponga al front, pero aquí queda.
    """
    return {
        "total": comments_db.get_total_comment_count(),
        "page": page,
        "limit": limit,
        "items": comments_db.get_latest_comments_head(limit, page),
    }
 
@router.get("/films/{imdb_id}/comments")
def film_comments(
    imdb_id: str = Path(pattern=IMDB_ID_PATTERN),
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1),
):
    """
    Comentarios de una película, paginados.
    Devuelve el total para que el frontend calcule las páginas.
    """
    return {
        "total": comments_db.get_film_comment_count(imdb_id),
        "page": page,
        "limit": limit,
        "items": comments_db.get_all_comments_film_head(imdb_id, limit, page),
    }
 
 
@router.get("/comments/{id_comentario}")
def comment_detail(id_comentario: int = Path(ge=1)):
    """
    Devuelve detalles de un comentario concreto por su ID.
    """
    comment = comments_db.get_comment(id_comentario)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comentario no encontrado.")
    return comment

@router.get("/users/{id_persona}/comments")
def user_comments(
    id_persona: int = Path(ge=1),
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1),
):
    """
    Comentarios de un usuario, paginados y con el nombre de cada película.
    Público: sirve tanto para el perfil de otro usuario como para el propio
    (el frontend obtiene su propio id con GET /users/me).
    """
    if users_db.get_public_by_id(id_persona) is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return {
        "total": comments_db.get_my_comment_count(id_persona),
        "page": page,
        "limit": limit,
        "items": comments_db.get_all_my_comments_head(id_persona, limit, page),
    }

# Endpoints protegidos

@router.post("/films/{imdb_id}/comments", status_code=status.HTTP_201_CREATED, tags=["protected"])
def post_comment(comment: CommentData,
                 imdb_id: str = Path(Pattern = IMDB_ID_PATTERN),
                 id_persona: int = Depends(get_current_user)):
    """
    Postea un comentario en una película.
    Importante no olvidar el patrón de imdb_id y estructurar bien el contenido de la petición.
    Se sube comment.content, que es el contenido en texto del objeto CommentData, lo que permite
    que haya compatibilidad entre el JSON y la base de datos.
    """
    comment_id = comments_db.add_comment(imdb_id, id_persona, comment.content)
    if comment_id is None:
        raise HTTPException(status_code=404, detail="Película no encontrada.")
    return comments_db.get_comment(comment_id)

@router.put("/comments/{comment_id}", tags=["protected"])
def edit_comment(comment: CommentData,
                 comment_id: int = Path(ge=1),
                 id_persona: int = Depends(get_current_user)):
    """
    Edita un comentario, comprobando para ello que el usuario que está editándolo es
    el creador original de éste.
    Se usa Path(ge=1) en el comment_id para que haga falta poner un id >= 1 en la url.
    """
    
    former_comment = comments_db.get_comment(comment_id)

    if former_comment is None:
        raise HTTPException(status_code=404, detail="Comentario no encontrado.")
    if former_comment["ID_PERSONA"] != id_persona:
        raise HTTPException(status_code=403, detail="No puedes editar el comentario de otra persona.")

    comments_db.edit_comment(comment_id, comment.content)
    return comments_db.get_comment(comment_id)

@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["protected"])
def del_comment(comment_id: int = Path(ge=1),
                id_persona: int = Depends(get_current_user)):
    """
    Borra un comentario de un usuario autenticado,
    devolviendo el status 204 que marca 'sin contenido'.
    """
    former_comment = comments_db.get_comment(comment_id)

    if former_comment is None:
        raise HTTPException(status_code=404, detail="Comentario no encontrado.")
    if former_comment["ID_PERSONA"] != id_persona:
        raise HTTPException(status_code=403, detail="No puedes borrar el comentario de otra persona.")

    comments_db.del_comment(comment_id)