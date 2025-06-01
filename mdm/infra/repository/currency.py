from typing import List

from sqlalchemy.orm import Session

from application.domain.entity.currency import CurrencyEntity
from application.usecase.create_currency import CreateCurrencyUseCase
from application.usecase.get_currency import GetCurrencyUseCase
from application.errors.error_handler import NotFoundError
from infra.repository.models.currency import Currency


class CurrencyRepository(CreateCurrencyUseCase, GetCurrencyUseCase):
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