from fastapi import FastAPI, Depends, Query
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from fastapi.requests import Request
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler
from typing import Annotated

#Import Jinja
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

#app = FastAPI()

def dependency1(param1: int):
     print("Global Dependency 1")

def dependency2():
     print("Global Dependency 2")

app = FastAPI(dependencies=[Depends(dependency1), Depends(dependency2)])

app.title = "My very App"
app.version = "0.0.1"

#Agregamos middleware creado por nosotros con Starlette
#app.add_middleware(HTTPErrorHandler)

#Creamos middleweare con FastApi
@app.middleware('http')
async def http_error_Handler(request:Request, call_next) -> Response | JSONResponse:
        print("Middleware is running")
        return await call_next(request) 

'''            try:
            return await call_next(request)
        except Exception as e:
            content = f"exc:{str(e)}"
            status_code =  status.HTTP_500_INTERNAL_SERVER_ERROR
            return JSONResponse(content, status_code=status_code)'''
        
# Usar path para unir directorios
static_path = os.path.join(os.path.dirname(__file__), 'static') # enlazamos el archivo actual con la carpeta static
template_path = os.path.join(os.path.dirname(__file__), 'templates')

#Montar el directorio static
app.mount('/static', StaticFiles(directory=static_path), 'static')
#Configurar carpeta templates
templates = Jinja2Templates(directory=template_path)


''' movies=[
    {
        "id":1,
        "title":"Avatar",
        "overview":"En un exuberante planeta llamado Pandora...",
        "year":"2009",
        "rating":7.8,
        "category":"Acción",
    },
    {
        "id":2,
        "title":"Matrix",
        "overview":"Pastilla roja o pastilla azul?",
        "year":"2000",
        "rating":9.9,
        "category":"Terror",
    }
]
'''


@app.get("/", tags=["Home"])
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request':request ,'message':'Welcome'})

#### Agregar Dependencias
'''def common_params(start_date : str, end_date : str):
     return {"start_date": start_date, "end_date": end_date}

CommonDep = Annotated[dict, Depends(common_params)]
'''

# crear dependencia mediante una clase
class CommonDep:
     def __init__(self, start_date : str, end_date : str) -> None:
          self.start_date = start_date
          self.end_date = end_date


@app.get('/users')
def get_users(commons: CommonDep = Depends()):
#def get_users(commons: Annotated[dict, Depends(common_params)]):
     return f"User created between {commons['start_date']} and {commons['end_date']}"

@app.get('/customers')
def get_customers(commons: CommonDep = Depends()):
     return f"Customer created between {commons['start_date']} and {commons['end_date']}"

###############

@app.get("/hello", tags=["Home"])
def home():
    return HTMLResponse('<h1>Hello World</h1>', status_code=200)

# incluye los routers
# se puede agregar un prefijo ej:/movies
# si se incluye el prefijo en esta router, se debe eliminar desde las rutas del movie_router.py
app.include_router(prefix = '/movies', router = movie_router)
