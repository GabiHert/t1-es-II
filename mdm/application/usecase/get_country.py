from abc import abstractmethod
from typing import Protocol, List

from application.domain.entity.country import CountryEntity


class GetCountryUseCase(Protocol):
    @abstractmethod
    def get_all(self) -> List[CountryEntity]:
        pass

    @abstractmethod
    def get_by_id(self, country_id: int) -> CountryEntity:
        pass 