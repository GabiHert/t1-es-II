from typing import Annotated

from pydantic import BaseModel, Field, confloat, conint, constr


class CountryDto(BaseModel):
    country_name: Annotated[str, Field(min_length=2, strip_whitespace=True)]
    numeric_code: Annotated[int, Field(ge=1)]
    capital_city: Annotated[str, Field(min_length=2, strip_whitespace=True)]
    population: Annotated[int, Field(ge=0)]
    area: Annotated[float, Field(ge=0)]

