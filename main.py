from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Huesped (BaseModel):
    id: int
    hab: int
    nombre: str
    edad: int
    ciudad: Optional[str] = None

personasList = []

@app.post("/huesped", response_model=Huesped)
def crear_huesped(person: Huesped):
    personasList.append(person)
    return person 

@app.get("/huesped", response_model=List[Huesped])
def get_huesped():
            return personasList

@app.get("/huesped/{huesped_hab}", response_model=Huesped)
def obtener_hab(huesped_hab: int):
    for hab in personasList:
        if huesped_hab == huesped_hab:
            return hab
    raise HTTPException(status_code=404, detail="huesped no encontrada")

@app.delete("/huesped/{persona_id}")
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
