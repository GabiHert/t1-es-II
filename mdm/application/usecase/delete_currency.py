from abc import ABC, abstractmethod

class DeleteCurrencyUseCase(ABC):
    @abstractmethod
    def delete(self, currency_id: int) -> None:
        """Delete a currency by its ID"""
        pass 