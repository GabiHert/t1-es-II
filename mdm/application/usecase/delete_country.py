from abc import ABC, abstractmethod

class DeleteCountryUseCase(ABC):
    @abstractmethod
    def delete(self, country_id: int) -> None:
        """Delete a country by its ID"""
        pass 