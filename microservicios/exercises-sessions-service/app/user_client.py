# services/user_client.py

import httpx
from fastapi import HTTPException

AUTH_SERVICE_URL = "http://auth-service:8001"  # Usa el puerto interno expuesto por el container del auth-service

async def validate_user_exists(user_id: str):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{AUTH_SERVICE_URL}/users/{user_id}")
        
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        elif response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error from auth service")
        
        return response.json()
    
    except httpx.RequestError as e:
        # Este error ocurre cuando no se puede conectar con el auth-service
        raise HTTPException(status_code=503, detail=f"User service not available: {e}")
