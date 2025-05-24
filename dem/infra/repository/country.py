from typing import List

from infra.repository.models.country import Country
from sqlalchemy.orm import Session

from application.domain.entity.country import CountryEntity
from application.usecase.create_country import CreateCountryUseCase
from application.usecase.get_country import GetCountryUseCase


class CountryRepository(CreateCountryUseCase, GetCountryUseCase):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, country_entity: CountryEntity) -> CountryEntity:
        country_model = Country(
            country_name=country_entity.country_name,
            numeric_code=country_entity.numeric_code,
            capital_city=country_entity.capital_city,
            population=country_entity.population,
            area=country_entity.area
        )

        self.db_session.add(country_model)
        self.db_session.commit()
        self.db_session.refresh(country_model)

        country_entity.country_id = country_model.country_id
        return country_entity

    def get_all(self) -> List[CountryEntity]:
        countries = self.db_session.query(Country).all()
        return [
            CountryEntity(
                country_id=country.country_id,
                country_name=country.country_name,
                numeric_code=country.numeric_code,
                capital_city=country.capital_city,
                population=country.population,
                area=country.area
            )
            for country in countries
        ]

    def get_by_id(self, country_id: int) -> CountryEntity:
        country = self.db_session.query(Country).filter(Country.country_id == country_id).first()
        if country is None:
            raise ValueError(f"Country with id {country_id} not found")
            
        return CountryEntity(
            country_id=country.country_id,
            country_name=country.country_name,
            numeric_code=country.numeric_code,
            capital_city=country.capital_city,
            population=country.population,
            area=country.area
        )