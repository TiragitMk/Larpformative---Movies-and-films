from urllib.parse import quote_plus
from backend.config import API_URL
import requests as r

if not API_URL:
    raise RuntimeError("API key or url not found. Please see 'README.md' and try again.")

def parse_title(str_title):
    """
    Quote_plus permite formatear un str a url, por ejemplo codificando
    signos reservados como &, ?, #, tildes, espacios...
    """
    parsed_result = quote_plus(str_title)
    return parsed_result

def parse_params(title:str="", year:int="", id:str="")->str:
    """
    Parsea los parámetros de función para que sean parámetros de query url.
    """
    if title:
        title = "t=" + parse_title(title)
        if year:
            year = "&y=" + str(year)
    elif id:
        id = "i=" + id

    return title + year + id + "&type=movie"

def is_in_api(title:str="", year:int="", id:str="")->bool:
    """
    Comprueba si el título o id introducidos existen en la api o no.
    Desconozco si es necesaria esta guarda, ya que la api tiene Response:bool.
    Depende del resto del código posterior.
    """
    request = r.get(API_URL + parse_params(title, year, id)).json()
    if request["Response"] == "False":
        print(request["Error"])
    return request["Response"] == "True"

def get_movie_api_data(movie_id:str="", movie_title:str="", movie_year:int=""):
    request = None
    if is_in_api(movie_title, movie_year, movie_id):
        request = r.get(API_URL + parse_params(movie_title, movie_year, movie_id)).json()
    return request

def search_movies_api(title:str, year:int="", page:int=1):
    """
    Busca películas por título en OMDb con el parámetro s=, que devuelve una LISTA de resultados
    (t= solo devuelve una). OMDb devuelve 10 resultados por página.
    Devuelve {"total": int, "items": [{Title, Year, imdbID, Type, Poster}, ...]}, o None si no hay resultados.
    Función customizable para añadir más información a los resultados de búsqueda.
    """
    params = "s=" + parse_title(title)
    if year:
        params += "&y=" + str(year)
    params += f"&page={page}&type=movie"
 
    data = r.get(API_URL + params, timeout=10).json()   # timeout: si OMDb no responde en 10 s, se corta.
    if data.get("Response") != "True":
        return None
    return {"total": int(data["totalResults"]), "items": data["Search"]}