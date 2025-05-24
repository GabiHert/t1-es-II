from abc import abstractmethod
from typing import Protocol

from application.domain.entity.country import CountryEntity


class CreateCountryUseCase(Protocol):
    @abstractmethod
    def create(self, country_entity: CountryEntity) -> CountryEntity:
        pass