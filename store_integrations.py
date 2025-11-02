import httpx
from config import settings
from models import StoreType
from typing import Dict

class StoreIntegration:
    @staticmethod
    async def deliver_to_store(store: StoreType, track_data: Dict, file_path: str) -> Dict:
        if store == StoreType.MTN:
            return await StoreIntegration._deliver_to_mtn(track_data, file_path)
        elif store == StoreType.VODACOM:
            return await StoreIntegration._deliver_to_vodacom(track_data, file_path)
        elif store == StoreType.TELKOM:
            return await StoreIntegration._deliver_to_telkom(track_data, file_path)
        else:
            raise ValueError(f"Unsupported store: {store}")
    
    @staticmethod
    async def _deliver_to_mtn(track_data: Dict, file_path: str) -> Dict:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {settings.mtn_api_key}"}
            
            with open(file_path, "rb") as f:
                files = {"audio": f}
                data = {
                    "title": track_data["title"],
                    "artist": track_data["artist"],
                    "duration": track_data["duration"]
                }
                
                response = await client.post(
                    f"{settings.mtn_api_url}/ringtones/upload",
                    headers=headers,
                    data=data,
                    files=files,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    return {"success": True, "data": response.json()}
                else:
                    return {"success": False, "error": response.text}
    
    @staticmethod
    async def _deliver_to_vodacom(track_data: Dict, file_path: str) -> Dict:
        return {"success": True, "data": {"message": "Vodacom delivery simulated"}}
    
    @staticmethod
    async def _deliver_to_telkom(track_data: Dict, file_path: str) -> Dict:
        return {"success": True, "data": {"message": "Telkom delivery simulated"}}
    
    @staticmethod
    async def fetch_analytics(store: StoreType, track_id: str) -> Dict:
        if store == StoreType.MTN:
            return await StoreIntegration._fetch_mtn_analytics(track_id)
        return {"plays": 0, "downloads": 0, "revenue": 0.0}
    
    @staticmethod
    async def _fetch_mtn_analytics(track_id: str) -> Dict:
        async with httpx.AsyncClient() as client:
            headers = {"Authorization": f"Bearer {settings.mtn_api_key}"}
            response = await client.get(
                f"{settings.mtn_api_url}/ringtones/{track_id}/analytics",
                headers=headers,
                timeout=30.0
            )
            
            if response.status_code == 200:
                return response.json()
            return {"plays": 0, "downloads": 0, "revenue": 0.0}
