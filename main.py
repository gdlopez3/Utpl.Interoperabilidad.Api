from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid
#seccion mongo_importar libreria
import pymongo
from fastapi_versioning import VersionedFastAPI, version
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from auth import authenticate


#configuracion de mongodb
cliente = pymongo.MongoClient("mongodb+srv://interuser:qwerty123@cluster0.eg0mcph.mongodb.net/?retryWrites=true&w=majority")
database = cliente ["checkin"]
coleccion = database["huespedes"]

description = """
Utpl tnteroperabilidad API ayuda a crear un huesped, buscar en la base y/o eliminarlo. 🚀

## Huesped

Tu puedes agragar un huesped.
Tu puedes listar los huespedes registrados.

"""
tags_metadata = [
    {
        "name":"huespedes",
        "description":"Permite realizar un crud completo de un huesped del hotel (listar)"
    }
]

app = FastAPI(
    title="Utpl Interoperabilidad APP - caso practico",
    description= description,
    version="semana 10",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Galo López",
        "url": "https://github.com/gdlopez3/Utpl.Interoperabilidad.Api.git",
        "email": "gdlopez3@utpl.edu.ec",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }, 
    openapi_tags = tags_metadata   
)

#para agregar seguridad a nuestro api
security = HTTPBasic()


class Huesped (BaseModel):
    id: str
    hab: int
    nombre: str
    edad: int
    ciudad: Optional[str] = None

class HuespedEntrada (BaseModel):
    hab: int
    nombre: str
    edad: int
    ciudad: Optional[str] = None


personasList = []

@app.post("/huesped", response_model=Huesped, tags = ["huespedes"])
@version(1,0)
async def crear_huesped(person: HuespedEntrada):
    print ('llego')
    itemHuesped = Huesped (id=str(uuid.uuid4()), hab = person.hab, nombre = person.nombre, edad = person.edad, ciudad = person.ciudad)
    resultadoBase = coleccion.insert_one(itemHuesped.dict())
    return itemHuesped

@app.get("/huesped", response_model=List[Huesped], tags = ["huespedes"])
@version(1,0)
def get_huesped():
    itemHuesped = list(coleccion.find()) ##devolver de l abase de datos.
    return itemHuesped

def get_huesped(credentials: HTTPBasicCredentials = Depends(security)):
    authenticate(credentials)
    items = list(coleccion.find())
    print (items)
    return items




## busqueda por id
@app.get("/huesped/{huesped_id}", response_model=Huesped, tags = ["huespedes"])
@version(1,0)
def obtener_huesped(huesped_id: str):
    item = coleccion.find_one({"id": huesped_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Huesped no encontrado")

## Agregar busqueda por hab.    
@app.get("/huesped/habitacion/{hab_num}", response_model=Huesped, tags = ["huespedes"])
@version(2,0)
def obtener_hab(hab_num: int):
    item = coleccion.find_one({"hab": hab_num})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Huesped no encontrado")

@app.delete("/huesped/{persona_id}", tags = ["huespedes"])
@version(1,0)
def eliminar_huesped (persona_id: int):
    persona = next((p for p in personasList if p.id == persona_id), None)
    if persona:
        personasList.remove(persona)
        return {"mensaje": "Persona Eliminada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    huesped_eliminado = personasList.pop(persona_id)

@app.get("/")
@version(1,0)
def read_root():
    return {"Hello": "TEST PARA LA APP EN LA NUBE ACTUALIZADO PARA CAPTURA DEBER"}


app = VersionedFastAPI(app)
