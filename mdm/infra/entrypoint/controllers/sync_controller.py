from typing import Dict
from application import SyncDataUseCase


class SyncController:
    def __init__(self, sync_data_usecase: SyncDataUseCase):
        self._sync_data_usecase = sync_data_usecase

    def sync(self) -> Dict:
        """
        Triggers the sync process and returns the extraction response.
        """
        return self._sync_data_usecase.sync()

# Create a default instance for Flask routes
sync_controller = SyncController(None)  # Will be properly initialized by the injector 