from abc import abstractmethod
from typing import Protocol

from domain.entity.currency import CurrencyEntity


class CreateCurrencyUseCase(Protocol):
    @abstractmethod
    def create(self, currency_entity: CurrencyEntity) -> CurrencyEntity:
        pass