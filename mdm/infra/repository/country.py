from typing import List

from infra.repository.models.country import Country
from sqlalchemy.orm import Session

from application.domain.entity.country import CountryEntity
from application.usecase.create_country import CreateCountryUseCase
from application.usecase.get_country import GetCountryUseCase
from application.usecase.delete_country import DeleteCountryUseCase
from application.usecase.update_country import UpdateCountryUseCase


class CountryRepository(CreateCountryUseCase, GetCountryUseCase, DeleteCountryUseCase, UpdateCountryUseCase):
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
        country_entity.created_at = country_model.created_at
        country_entity.updated_at = country_model.updated_at
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
                area=country.area,
                created_at=country.created_at,
                updated_at=country.updated_at
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
            area=country.area,
            created_at=country.created_at,
            updated_at=country.updated_at
        )

    def get_by_numeric_code(self, numeric_code: int) -> CountryEntity:
        country = self.db_session.query(Country).filter(Country.numeric_code == numeric_code).first()
        if country is None:
            raise ValueError(f"Country with numeric code {numeric_code} not found")
            
        return CountryEntity(
            country_id=country.country_id,
            country_name=country.country_name,
            numeric_code=country.numeric_code,
            capital_city=country.capital_city,
            population=country.population,
            area=country.area,
            created_at=country.created_at,
            updated_at=country.updated_at
        )

    def delete(self, country_id: int) -> None:
        country = self.db_session.query(Country).filter(Country.country_id == country_id).first()
        if country is None:
            raise ValueError(f"Country with id {country_id} not found")
        
        self.db_session.delete(country)
        self.db_session.commit()

    def update(self, country_id: int, country_entity: CountryEntity) -> CountryEntity:
        country = self.db_session.query(Country).filter(Country.country_id == country_id).first()
        if country is None:
            raise ValueError(f"Country with id {country_id} not found")
        
        # Update only the fields that are provided
        if country_entity.country_name is not None:
            country.country_name = country_entity.country_name
        if country_entity.numeric_code is not None:
            country.numeric_code = country_entity.numeric_code
        if country_entity.capital_city is not None:
            country.capital_city = country_entity.capital_city
        if country_entity.population is not None:
            country.population = country_entity.population
        if country_entity.area is not None:
            country.area = country_entity.area
        if country_entity.updated_at is not None:
            country.updated_at = country_entity.updated_at
        
        self.db_session.commit()
        self.db_session.refresh(country)
        
        return CountryEntity(
            country_id=country.country_id,
            country_name=country.country_name,
            numeric_code=country.numeric_code,
            capital_city=country.capital_city,
            population=country.population,
            area=country.area,
            created_at=country.created_at,
            updated_at=country.updated_at
        )