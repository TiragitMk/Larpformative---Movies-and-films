from typing import Literal
from fastapi import APIRouter, HTTPException, Path, Query
from backend.omdb_requests.omdb_requests_services import get_movie_api_data, search_movies_api
from backend.sql_model import films as films_db
from backend.sql_model import ratings as ratings_db
from backend.sql_model import comments as comments_db
 
router = APIRouter(prefix="/films", tags=["films"])
 
IMDB_ID_PATTERN = r"^tt\d{7,8}$"        # Patrón del imdb_id, tt seguido de 7-8 números.
 
 
@router.get("/search")
def search_film(
    imdb_id: str | None = Query(None, pattern=IMDB_ID_PATTERN),
    title: str | None = Query(None, min_length=1),
    year: int | None = Query(None, ge=1880, le=2100),
):
    """
    Busca una película en OMDb bien por imdb_id, o bien por título (y año opcional).
    Si llegan ambos tiene prioridad el imdb_id.
    Usa Query para afinar con reglas de validación los parámetros de los endpoints.
    """
    if not imdb_id and not title:
        raise HTTPException(status_code=400, detail="Submit imdb_id or title.")
 
    if imdb_id:
        data = get_movie_api_data(movie_id=imdb_id)
    else:
        data = get_movie_api_data(movie_title=title, movie_year=year or "")
 
    if data is None:
        raise HTTPException(status_code=404, detail="Movie not found.")
    return data

@router.get("/search/list")
def search_film_list(
    title: str = Query(min_length=1),
    year: int | None = Query(None, ge=1880, le=2100),
    page: int = Query(1, ge=1, le=100),
):
    """
    Busca en OMDB todas las películas cuyo título contenga el texto, 10 por página.
    Es la búsqueda pensada para el buscador de la web.
    Cada resultado trae imdb_ID, que el frontend usa para tener los detalles después.
    OJO: La búsqueda no funciona si se añade el año, pues es un buscador sólo de título. BORRAR O NO USAR AÑO EN EL FRONTEND.
    """
    result = search_movies_api(title, year or "", page)
    if result is None:
        raise HTTPException(status_code=404, detail="Couldn't find any movies.")
    return {"total": result["total"], "page": page, "limit": 10, "items": result["items"]}
 
 
@router.get("")
def list_films(
    order_by: Literal["rating", "year"] = "rating",
    order: Literal["ASC", "DESC"] = "DESC",
    limit: int = Query(10, ge=1, le=50),
    page: int = Query(1, ge=1),
):
    """
    Lista las películas registradas en la db (las que tienen algún comentario o calificación).
    order se valida con Literal porque en sql_model se inserta con f-string. Así se evita inyección SQL.
    PROBABLEMENTE NO SE USARÁ EN EL DISEÑO FINAL. Para usarla haría falta cierta escala (una db de películas
    bastante llena de entradas) y no me merece la pena meterlo. Funciona, pero no está en el frontend.
    """
    if order_by == "rating":
        films = films_db.get_all_films_by_rating_head(order, limit, page)
    else:
        films = films_db.get_all_films_by_year_head(order, limit, page)

    return {"total": films_db.get_film_count(), "page": page, "limit": limit, "films": films}
 
 
@router.get("/{imdb_id}")
def film_detail(imdb_id: str = Path(pattern=IMDB_ID_PATTERN)):
    """
    Detalle de una película: datos de OMDb, promedio de calificaciones y número de comentarios.
    Los comentarios se piden aparte y paginados en GET /films/{imdb_id}/comments.
    """
    data = get_movie_api_data(movie_id=imdb_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Movie not found.")
 
    return {
        "film": data,
        "rating": ratings_db.get_average_rating(imdb_id),
        "comment_count": comments_db.get_film_comment_count(imdb_id),
    }
 