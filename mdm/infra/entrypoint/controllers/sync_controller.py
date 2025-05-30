from typing import Dict
from application.usecase.sync_data import SyncDataUseCase


class SyncController:
    def __init__(self, sync_data_usecase: SyncDataUseCase):
        self._sync_data_usecase = sync_data_usecase

    def sync(self) -> Dict:
        """
        Triggers the sync process and returns the extraction response.
        """
        return self._sync_data_usecase.sync() 