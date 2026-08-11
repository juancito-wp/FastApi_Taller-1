from fastapi import FastAPI, HTTPException
from src.models import trainee_model
from src.services.rick_morty_api import (
    fetch_character_by_id,
    fetch_random_character,
)

app = FastAPI(title="Rick and Morty API Service")

# ==========================================
# RICK AND MORTY API
# ==========================================


@app.get("/")
async def root():
    return {"message": "¡Bienvenido a la API de Rick and Morty!"}


@app.get("/character/random")
async def get_random_character():
    character = await fetch_random_character()
    if not character:
        raise HTTPException(
            status_code=500, detail="Error al consultar la API externa"
        )

    return character


@app.get("/character/{character_id}")
async def get_character(character_id: int):
    if character_id < 1 or character_id > 826:
        raise HTTPException(
            status_code=400,
            detail="El ID del personaje debe estar entre 1 y 826.",
        )

    character = await fetch_character_by_id(character_id)

    if not character:
        raise HTTPException(
            status_code=404, detail="Personaje no encontrado"
        )

    return character


# ==========================================
# GESTIÓN DE APRENDICES
# ==========================================


@app.get("/trainees")
async def get_trainees():
    """Obtiene todos los aprendices registrados."""
    trainees = trainee_model.load_trainees()
    return trainees


@app.get("/trainees/{document}")
async def get_trainee(document: str):
    """Obtiene un aprendiz por su número de documento."""
    trainee = trainee_model.search_by_document(document)

    if not trainee:
        raise HTTPException(
            status_code=404, detail="Aprendiz no encontrado"
        )

    return trainee


@app.post("/trainees")
async def create_trainee(data: dict):
    """Registra un nuevo aprendiz."""
    document = data.get("documento")

    if not document:
        raise HTTPException(
            status_code=400, detail="El número de documento es obligatorio"
        )

    existing_trainee = trainee_model.search_by_document(document)

    if existing_trainee:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un aprendiz con este número de documento",
        )

    trainee_model.register_trainee(data)

    return {"message": "Aprendiz registrado exitosamente", "trainee": data}


@app.put("/trainees/{document}")
async def update_trainee(document: str, data: dict):
    """Actualiza los datos de un aprendiz."""
    updated = trainee_model.update_trainee(document, data)

    if not updated:
        raise HTTPException(
            status_code=404, detail="Aprendiz no encontrado"
        )

    return {"message": "Aprendiz actualizado exitosamente"}


@app.delete("/trainees/{document}")
async def delete_trainee(document: str):
    """Elimina un aprendiz."""
    deleted = trainee_model.delete_trainee(document)

    if not deleted:
        raise HTTPException(
            status_code=404, detail="Aprendiz no encontrado"
        )

    return {"message": "Aprendiz eliminado exitosamente"}


@app.get("/trainees/search/{term}")
async def search_trainees(term: str):
    """Busca aprendices por nombre o número de ficha."""
    results = trainee_model.search_trainees_by_term(term)

    if not results:
        raise HTTPException(
            status_code=404, detail="No se encontraron aprendices"
        )

    return results