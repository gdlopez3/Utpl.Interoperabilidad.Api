from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Persona (BaseModel):
    id: int
    nombre: str
    edad: int
    ciudad: Optional[str] = None

personasList = []

@app.post("/personas", response_model=Persona)
def crear_persona(person: Persona):
    personasList.append(person)
    return person 

@app.get("/personas", response_model=List[Persona])
def get_personas():
            return personasList

@app.get("/personas/{persona_id}", response_model=Persona)
def obtener_persona(persona_id: int):
    for persona in personasList:
        if persona.id == persona_id:
            return persona
    raise HTTPException(status_code=404, detail="persona no encontrada")

@app.get("/")
def read_root():
    return {"Hello": "Interoperabilidad 5"}
