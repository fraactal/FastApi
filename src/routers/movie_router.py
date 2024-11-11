
from typing import List
from fastapi import Query, Path, APIRouter
from fastapi.responses import FileResponse, JSONResponse

from src.models.movie_model import Movie, MovieUpdate, MovieCreate


movies: List[Movie] = []

# se agrega el router para que los path tengan la nomenclatura y se puedan agregar desde el archivo Main
movie_router = APIRouter()

# se puede especificar el squema que queremos retornar
# se especifica la clase List de libreria typing y se le pasa la clase Movie
@movie_router.get("/", tags=["Movies"], status_code=200, response_description="Nos debe devolver una respuesta exitosa")
def get_movies() -> List[Movie]:
    #return movies   #--> retorna el objeto dictionary
    # return [movie.model_dump() for movie in movies] #--> retorna objeto en formato json con el metodo model_dump
    content = [movie.model_dump() for movie in movies] #--> retorna objeto en formato json con el metodo model_dump

    return JSONResponse(content=content, status_code=200)


#envío parametros por URL
@movie_router.get("/{id}", tags=["Movies"])
def get_movie(id: int = Path(gt=0)) -> Movie  | dict:
    for movie in movies:
        if (movie.id == id):
            return JSONResponse(content=movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)
   
    
# Params Query -> va la clave y el valor
# localhost:5000/movies/?id=2
# se agrega un slash al final porque es la que se trabajará con parametros query
@movie_router.get("/by_category", tags=["Movies"])
def get_movie_by_category(category: str = Query(min_length=5, max_length=20)) -> Movie | dict:
    for movie in movies:
        if (movie.category == category):
            return JSONResponse(content=movie.model_dump(), status_code=200)
    return JSONResponse(content={}, status_code=404)


# Pasar los valores por el request body con fastApi -> Body
@movie_router.post('/', tags=['Movies'])
def create_movie(movie: MovieCreate) -> List[Movie]:
    #se convierte a tipo diccionario para poder almacenarlo en el arreglo movies de ejemplo
    movies.append(movie)
    content = [movie.model_dump() for movie in movies] #--> retorna objeto en formato json con el metodo model_dump
    # Al hacer una creacion es codigo 201
    return JSONResponse(content=content, status_code=201)

    #redirect Response
    #return RedirectResponse('/movies', status_code= 303)

#Modificacion, 
#Se envía por parmetro el ID Que no es parte del body
@movie_router.put('/{id}', tags=["Movies"])
def update_movies (id:int, movie:MovieUpdate) -> List[Movie]:
    for item in movies:
        if (item.id == id):
            item.title = movie.title
            item.overview = movie.overview
            item.year = movie.year
            item.rating = movie.rating
            item.category = movie.category
        content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

#Eliminar
@movie_router.delete('/{id}', tags=["Movies"])
def delete_movie(id:int) -> List[Movie]:
    for movie in movies:
        if (movie.id == id):
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)

#File Response
@movie_router.get('/get_file', tags=["Movies"])
def get_file():
    content = [movie.model_dump() for movie in movies]
    data = pd.DataFrame(content)
    #print(data)
    data.to_csv("my_movies.csv", index =False)
    return FileResponse("my_movies.csv", status_code=200)