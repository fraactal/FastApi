import datetime
from pydantic import BaseModel, Field, field_validator



#Para consultar y registrar
class Movie(BaseModel):
   #id: Optional[int] = None # se puede agregar un valor de tipo opcional usando la libreria Typing
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category:str


# para actualizar
class MovieUpdate(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category:str


#añadir validaciones con la clase Field
class MovieCreate(BaseModel):
    id: int
    #title: str = Field(min_length=5, max_length=15)
    title: str
    overview: str = Field(min_length=15, max_length=50)
    #gt greater than, ge greater than or equal, lt less than, le less than or equal
    year: int = Field(le=datetime.date.today().year, ge= 1900)
    rating: float = Field(ge=0,le=10, default=10)
    category:str = Field(min_length=5, max_length=20)

    model_config = {
        'json_schema_extra':{
            'example':{
                'id': 10,
                'title':'My movie',
                'overview': 'Esta pelicula trata acerca de...',
                'year': 2022,
                'rating':5,
                'category':'Terror'
            }
        }
    }

## Validacion de mensajes personalizados
    #@validator('title')
    @field_validator('title')
    def validate_title(cls, value):
        if len(value) < 5:
            raise ValueError('El título debe tener al menos 5 caracteres')
        if len(value) > 15:
            raise ValueError('El título debe tener maximo 15 caracteres')
        return value

