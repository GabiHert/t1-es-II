from typing import Annotated

from pydantic import BaseModel, Field


class CurrencyDto(BaseModel):
    currency_code: Annotated[str, Field(min_length=1, max_length=10, strip_whitespace=True)]
    currency_name: Annotated[str, Field(min_length=2, strip_whitespace=True)]
    currency_symbol: Annotated[str, Field(min_length=1, strip_whitespace=True)]
    country_id: Annotated[int, Field(ge=1)]