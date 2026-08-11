import random
import httpx

API_URL = "https://rickandmortyapi.com/api/character"


async def fetch_character_by_id(character_id: int):
    """Obtiene la información de un personaje según su ID."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{API_URL}/{character_id}", timeout=5.0
            )
            response.raise_for_status()
            data = response.json()

            return {
                "id": data.get("id"),
                "name": data.get("name"),
                "species": data.get("species"),
                "status": data.get("status"),
                "image": data.get("image"),
            }
        except httpx.HTTPError as e:
            print(f"Error al consultar la API externa: {e}")
            return None


async def fetch_random_character():
    """Genera un ID aleatorio y retorna el personaje."""
    random_id = random.randint(1, 826)
    return await fetch_character_by_id(random_id)