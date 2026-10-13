from fastapi import APIRouter, Path, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from backend.dependencies import get_current_user
from backend.sql_model import ratings as ratings_db
from backend.sql_model import users as users_db
from backend.fastapi_routers.films_rt import IMDB_ID_PATTERN
 
router = APIRouter(tags=["ratings"])

class RatingData(BaseModel):
    """
    Cuerpo JSON para calificar: {"rating": 4}. Fuera de 1-5, FastAPI responde 422.
    """
    rating: int = Field(ge=1, le=5)
 
 
@router.get("/films/{imdb_id}/rating")
def film_rating(imdb_id: str = Path(pattern=IMDB_ID_PATTERN)):
    """
    Promedio y número de calificaciones de una película. average es 0 si no tiene ninguna (el mínimo válido es 1).
    """
    stats = ratings_db.get_average_rating(imdb_id)
    return {"imdb_id": imdb_id, "average": stats["average"], "count": stats["count"]}

@router.get("/users/{id_persona}/ratings")
def user_ratings(
    id_persona: int = Path(ge=1),
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1),
):
    """
    Calificaciones de un usuario paginadas y con el nombre de cada película.
    """
    if users_db.get_public_by_id(id_persona) is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")
    return {
        "total": ratings_db.get_user_rating_count(id_persona),
        "page": page,
        "limit": limit,
        "items": ratings_db.get_user_ratings_head(id_persona, limit, page),
    }

# Endpoints protegidos

@router.get("/films/{imdb_id}/rating/me", tags=["protected"])
def my_film_rating(imdb_id: str = Path(pattern=IMDB_ID_PATTERN),
                   id_persona: int = Depends(get_current_user)):
    """
    Calificación en una película del usuario autenticado, o null si no la ha calificado.
    Sirve para marcar las estrellas ya elegidas al abrir el detalle de la película.
    Devuelve null en vez de 404 porque "no calificada" es un estado normal, no un error.
    """
    return {"imdb_id": imdb_id, "my_rating": ratings_db.get_rating(id_persona, imdb_id)}

@router.put("/films/{imdb_id}/rating/me", tags=["protected"])
def rate_film(data: RatingData,
              imdb_id: str = Path(pattern=IMDB_ID_PATTERN),
              id_persona: int = Depends(get_current_user)):
    """
    Pone o cambia la calificación del usuario autenticado (add_rating hace ON CONFLICT DO UPDATE).
    Es PUT y no POST porque repetir la misma petición deja el mismo resultado.
    Devuelve la calificación propia y el promedio actualizado para que el frontend lo refresque
    sin tener que hacer otra petición.
    Como el rating va en el cuerpo de la petición, no se puede olvidar llamar al atributo .rating
    de la clase heredada de BaseModel, que llama al campo concreto del JSON.
    """
    if ratings_db.add_rating(imdb_id, id_persona, data.rating) is None:
        raise HTTPException(status_code=404, detail="Película no encontrada.")
    stats = ratings_db.get_average_rating(imdb_id)
    return {"imdb_id": imdb_id, "my_rating": data.rating, "average": stats["average"], "count": stats["count"]}

@router.delete("/films/{imdb_id}/rating/me", tags=["protected"])
def delete_my_rating(imdb_id: str = Path(pattern=IMDB_ID_PATTERN),
                     id_persona: int = Depends(get_current_user)):
    """
    Quita la calificación del usuario autenticado. 404 si no había calificado la película.
    No hace falta comprobar el dueño (403), porque la consulta borra solo
    la fila de este id_persona, sólo hay una combinación rating-usuario.
    """
    if not ratings_db.del_rating(id_persona, imdb_id):
        raise HTTPException(status_code=404, detail="No has calificado esta película.")