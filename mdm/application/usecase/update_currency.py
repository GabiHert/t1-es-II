from abc import ABC, abstractmethod
from application.domain.entity.currency import CurrencyEntity

class UpdateCurrencyUseCase(ABC):
    @abstractmethod
    def update(self, currency_id: int, currency_entity: CurrencyEntity) -> CurrencyEntity:
        """Update a currency by its ID"""
        pass 