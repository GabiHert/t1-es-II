from abc import abstractmethod
from typing import Protocol, List

from application.domain.entity.currency import CurrencyEntity


class GetCurrencyUseCase(Protocol):
    @abstractmethod
    def get_all(self) -> List[CurrencyEntity]:
        pass

    @abstractmethod
    def get_by_id(self, currency_id: int) -> CurrencyEntity:
        pass

    @abstractmethod
    def get_by_code(self, currency_code: str) -> CurrencyEntity:
        pass 