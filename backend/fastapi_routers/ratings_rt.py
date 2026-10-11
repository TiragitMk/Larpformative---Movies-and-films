from fastapi import APIRouter, Path
from backend.sql_model import ratings as ratings_db
from backend.fastapi_routers.films_rt import IMDB_ID_PATTERN
 
router = APIRouter(tags=["ratings"])
 
 
@router.get("/films/{imdb_id}/rating")
def film_rating(imdb_id: str = Path(pattern=IMDB_ID_PATTERN)):
    """
    Promedio y número de calificaciones de una película. average es 0 si no tiene ninguna (el mínimo válido es 1).
    """
    stats = ratings_db.get_average_rating(imdb_id)
    return {"imdb_id": imdb_id, "average": stats["average"], "count": stats["count"]}