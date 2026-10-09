from backend.config import API_URL
import requests as r

if not API_URL:
    raise RuntimeError("API key or url not found. Please see 'README.md' and try again.")

def parse_title(str_title):
    parsed_result = str_title.replace(" ","+")
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