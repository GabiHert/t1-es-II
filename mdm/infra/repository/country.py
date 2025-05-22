from models.country import Country
from sqlalchemy.orm import Session

from application.domain.entity.country import CountryEntity
from application.usecase.create_country import CreateCountryUseCase


class CountryRepository(CreateCountryUseCase):
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