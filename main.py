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
def crear_persona(person: Huesped):
    personasList.append(person)
    return person 

@app.get("/huesped", response_model=List[Huesped])
def get_personas():
            return personasList

@app.get("/huesped/{persona_id}", response_model=Huesped)
def obtener_persona(persona_id: int):
    for persona in personasList:
        if persona.id == persona_id:
            return persona
    raise HTTPException(status_code=404, detail="persona no encontrada")

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
