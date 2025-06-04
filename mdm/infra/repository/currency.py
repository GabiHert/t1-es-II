from typing import List
from datetime import datetime

from sqlalchemy.orm import Session

from application.domain.entity.currency import CurrencyEntity
from application.usecase.create_currency import CreateCurrencyUseCase
from application.usecase.get_currency import GetCurrencyUseCase
from application.usecase.delete_currency import DeleteCurrencyUseCase
from application.usecase.update_currency import UpdateCurrencyUseCase
from application.errors.error_handler import NotFoundError
from infra.repository.models.currency import Currency


class CurrencyRepository(CreateCurrencyUseCase, GetCurrencyUseCase, DeleteCurrencyUseCase, UpdateCurrencyUseCase):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, currency_entity: CurrencyEntity) -> CurrencyEntity:
        currency_model = Currency(
            currency_code=currency_entity.currency_code,
            currency_name=currency_entity.currency_name,
            currency_symbol=currency_entity.currency_symbol,
            country_id=currency_entity.country_id
        )

        self.db_session.add(currency_model)
        self.db_session.commit()
        self.db_session.refresh(currency_model)

        currency_entity.currency_id = currency_model.currency_id
        currency_entity.created_at = currency_model.created_at
        currency_entity.updated_at = currency_model.updated_at
        return currency_entity

    def get_all(self) -> List[CurrencyEntity]:
        currencies = self.db_session.query(Currency).all()
        return [
            CurrencyEntity(
                currency_id=currency.currency_id,
                currency_code=currency.currency_code,
                currency_name=currency.currency_name,
                currency_symbol=currency.currency_symbol,
                country_id=currency.country_id,
                created_at=currency.created_at,
                updated_at=currency.updated_at
            )
            for currency in currencies
        ]

    def get_by_id(self, currency_id: int) -> CurrencyEntity:
        currency = self.db_session.query(Currency).filter(Currency.currency_id == currency_id).first()
        if currency is None:
            raise NotFoundError(f"Currency with id {currency_id} not found")
            
        return CurrencyEntity(
            currency_id=currency.currency_id,
            currency_code=currency.currency_code,
            currency_name=currency.currency_name,
            currency_symbol=currency.currency_symbol,
            country_id=currency.country_id,
            created_at=currency.created_at,
            updated_at=currency.updated_at
        )

    def get_by_code(self, currency_code: str) -> CurrencyEntity:
        currency = self.db_session.query(Currency).filter(Currency.currency_code == currency_code).first()
        if currency is None:
            raise NotFoundError(f"Currency with code {currency_code} not found")
            
        return CurrencyEntity(
            currency_id=currency.currency_id,
            currency_code=currency.currency_code,
            currency_name=currency.currency_name,
            currency_symbol=currency.currency_symbol,
            country_id=currency.country_id,
            created_at=currency.created_at,
            updated_at=currency.updated_at
        )

    def delete(self, currency_id: int) -> None:
        currency = self.db_session.query(Currency).filter(Currency.currency_id == currency_id).first()
        if currency is None:
            raise NotFoundError(f"Currency with id {currency_id} not found")
        
        self.db_session.delete(currency)
        self.db_session.commit()

    def update(self, currency_id: int, currency_entity: CurrencyEntity) -> CurrencyEntity:
        currency = self.db_session.query(Currency).filter(Currency.currency_id == currency_id).first()
        if currency is None:
            raise NotFoundError(f"Currency with id {currency_id} not found")
        
        # Update only the fields that are provided
        if currency_entity.currency_code is not None:
            currency.currency_code = currency_entity.currency_code
        if currency_entity.currency_name is not None:
            currency.currency_name = currency_entity.currency_name
        if currency_entity.currency_symbol is not None:
            currency.currency_symbol = currency_entity.currency_symbol
        if currency_entity.country_id is not None:
            currency.country_id = currency_entity.country_id
        
        # Handle timestamps
        if currency_entity.created_at is not None:
            currency.created_at = datetime.fromisoformat(currency_entity.created_at) if isinstance(currency_entity.created_at, str) else currency_entity.created_at
        if currency_entity.updated_at is not None:
            currency.updated_at = datetime.fromisoformat(currency_entity.updated_at) if isinstance(currency_entity.updated_at, str) else currency_entity.updated_at
            
        self.db_session.commit()
        self.db_session.refresh(currency)
        
        return CurrencyEntity(
            currency_id=currency.currency_id,
            currency_code=currency.currency_code,
            currency_name=currency.currency_name,
            currency_symbol=currency.currency_symbol,
            country_id=currency.country_id,
            created_at=currency.created_at,
            updated_at=currency.updated_at
        )