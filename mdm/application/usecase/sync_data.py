import requests
from datetime import datetime
from typing import Dict, Optional

from config.api.dem_config import INJECTIONS_ENDPOINT, EXTRACTIONS_ENDPOINT


class SyncDataUseCase:
    def sync(self) -> Dict:
        """
        Fetches the latest injection and triggers a new extraction.
        Returns the extraction response.
        """
        # Step 1: Fetch injections
        response = requests.get(INJECTIONS_ENDPOINT)
        response.raise_for_status()
        injections = response.json()

        # Step 2: Find latest injection
        latest_injection = self._get_latest_injection(injections)
        if not latest_injection:
            raise ValueError("No injections found")

        # Step 3: Trigger extraction
        extraction_response = requests.post(
            EXTRACTIONS_ENDPOINT,
            json={
                "service": "mdm",
                "injection_id": latest_injection["id"]
            }
        )
        extraction_response.raise_for_status()
        
        # Step 4: Return extraction response
        return extraction_response.json()

    def _get_latest_injection(self, injections: list) -> Optional[Dict]:
        """Find the injection with the most recent created_at timestamp."""
        if not injections:
            return None
            
        return max(
            injections,
            key=lambda x: datetime.fromisoformat(x["created_at"])
        ) 