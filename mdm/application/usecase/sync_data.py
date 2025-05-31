import requests
from datetime import datetime
from typing import Dict, Optional

from config.api.dem_config import DEM_ENDPOINT  

class SyncDataUseCase:
    def sync(self) -> Dict:
        """
        Fetches the latest extraction and triggers a new load.
        Returns the extraction response.
        """
        # Step 1: Fetch extractions
        response = requests.get(DEM_ENDPOINT+"/source/restcountries/extractions")
        response.raise_for_status()
        extractions = response.json()

        # Step 2: Find latest extraction
        latest_extraction = self._get_latest_extraction(extractions)
        if not latest_extraction:
            raise ValueError("No extraction found")

        # Step 3: Trigger extraction
        load_response = requests.post(
            DEM_ENDPOINT+"/loads",
            json={
                "service": "mdm",
                "extraction_id": latest_extraction["extraction_id"]
            }
        )
        load_response.raise_for_status()
        
        # Step 4: Return extraction response
        return load_response.json()

    def _get_latest_extraction(self, extractions: list) -> Optional[Dict]:
        """Find the extraction with the most recent created_at timestamp."""
        if not extractions:
            return None
            
        return max(
            extractions,
            key=lambda x: datetime.fromisoformat(x["created_at"])
        ) 