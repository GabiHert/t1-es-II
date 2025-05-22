from models.currency import Currency
from sqlalchemy.orm import Session

from application.domain.entity.currency import CurrencyEntity
from application.usecase.create_currency import CreateCurrencyUseCase


class CurrencyRepository(CreateCurrencyUseCase):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, country_entity: CurrencyEntity) -> CurrencyEntity:
        currency_model = Currency(
            currency_code=country_entity.currency_code,
            currency_name=country_entity.currency_name,
            currency_symbol=country_entity.currency_symbol,
            country_id=country_entity.country_id
        )

        self.db_session.add(currency_model)
        self.db_session.commit()
        self.db_session.refresh(currency_model)

        country_entity.currency_id = currency_model.currency_id
        return country_entity