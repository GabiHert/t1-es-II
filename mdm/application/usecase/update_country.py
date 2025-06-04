from abc import ABC, abstractmethod
from application.domain.entity.country import CountryEntity

class UpdateCountryUseCase(ABC):
    @abstractmethod
    def update(self, country_id: int, country_entity: CountryEntity) -> CountryEntity:
        """Update a country by its ID"""
        pass 