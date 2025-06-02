from typing import Annotated

from pydantic import BaseModel, Field

from application.domain.entity.currency import CurrencyEntity


class CurrencyDTO(BaseModel):
    currency_code: Annotated[str, Field(min_length=1, max_length=10, strip_whitespace=True)]
    currency_name: Annotated[str, Field(min_length=2, strip_whitespace=True)]
    currency_symbol: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    country_id: Annotated[int, Field(ge=1)]

    def to_entity(self) -> CurrencyEntity:
        return CurrencyEntity(
            currency_code=self.currency_code,
            currency_name=self.currency_name,
            currency_symbol=self.currency_symbol,
            country_id=self.country_id
        )

    @classmethod
    def from_entity(cls, entity: CurrencyEntity) -> "CurrencyDTO":
        return cls(
            currency_code=entity.currency_code,
            currency_name=entity.currency_name,
            currency_symbol=entity.currency_symbol,
            country_id=entity.country_id
        )