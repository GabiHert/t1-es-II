from typing import Annotated

from pydantic import BaseModel, Field, confloat, conint, constr

from application.domain.entity.country import CountryEntity


class CountryDto(BaseModel):
    country_name: Annotated[str, Field(min_length=2, strip_whitespace=True)]
    numeric_code: Annotated[int, Field(ge=1)]
    capital_city: Annotated[str, Field(min_length=2, strip_whitespace=True)]
    population: Annotated[int, Field(ge=0)]
    area: Annotated[float, Field(ge=0)]

    def to_entity(self) -> CountryEntity:
        return CountryEntity(
            country_name=self.country_name,
            numeric_code=self.numeric_code,
            capital_city=self.capital_city,
            population=self.population,
            area=self.area
        )

    def from_entity(cls, entity: CountryEntity) -> "CountryDto":
        return cls(
            country_name=entity.country_name,
            numeric_code=entity.numeric_code,
            capital_city=entity.capital_city,
            population=entity.population,
            area=entity.area
        )