from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
#seccion mongo_importar libreria
import pymongo

#configuracion de mongodb
cliente = pymongo.MongoClient("mongodb+srv://gdlopez3:Emilia1707.@cluster0.eg0mcph.mongodb.net/?retryWrites=true&w=majority")
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
async def crear_huesped(person: HuespedEntrada):
    print ('llego')
    itemHuesped = Huesped (id=str(uuid.uuid4()), hab = person.hab, nombre = person.nombre, edad = person.edad, ciudad = person.ciudad)
    resultadoBase = coleccion.insert_one(itemHuesped.dict())
    return itemHuesped

@app.get("/huesped", response_model=List[Huesped], tags = ["huespedes"])
def get_huesped():
            return personasList

@app.get("/huesped/{huesped_hab}", response_model=Huesped, tags = ["huespedes"])
def obtener_hab(huesped_hab: int):
    for hab in personasList:
        if huesped_hab == huesped_hab:
            return hab
    raise HTTPException(status_code=404, detail="huesped no encontrada")

@app.delete("/huesped/{persona_id}", tags = ["huespedes"])
def eliminar_huesped (persona_id: int):
    persona = next((p for p in personasList if p.id == persona_id), None)
    if persona:
        personasList.remove(persona)
        return {"mensaje": "Persona Eliminada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    huesped_eliminado = personasList.pop(persona_id)

@app.get("/")
def read_root():
    return {"Hello": "TEST PARA LA APP EN LA NUBE ACTUALIZADO PARA CAPTURA DEBER"}
