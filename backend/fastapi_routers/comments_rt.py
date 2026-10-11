from fastapi import APIRouter, HTTPException, Path, Query
from backend.sql_model import comments as comments_db
from backend.fastapi_routers.films_rt import IMDB_ID_PATTERN
 
router = APIRouter(tags=["comments"])
 
 
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
 