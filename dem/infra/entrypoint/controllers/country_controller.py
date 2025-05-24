from typing import Dict, List

from application.domain.entity.country import CountryEntity
from application.errors.error_handler import MissingFieldError, InvalidFieldError
from application.usecase.create_country import CreateCountryUseCase
from application.usecase.get_country import GetCountryUseCase


class CountryController:
    def __init__(
        self,
        create_country_usecase: CreateCountryUseCase,
        get_country_usecase: GetCountryUseCase
    ):
        self._create_country_usecase = create_country_usecase
        self._get_country_usecase = get_country_usecase

    def create_country(self, country_data: Dict) -> Dict:
        required_fields = ["country_name", "numeric_code", "capital_city", "population", "area"]
        for field in required_fields:
            if field not in country_data:
                raise MissingFieldError(f"The field '{field}' is required")

        try:
            country_entity = CountryEntity(
                country_name=country_data["country_name"],
                numeric_code=country_data["numeric_code"],
                capital_city=country_data["capital_city"],
                population=country_data["population"],
                area=country_data["area"]
            )
        except ValueError as e:
            raise InvalidFieldError(str(e))

        created_country = self._create_country_usecase.create(country_entity)
        return {
            "country_id": created_country.country_id,
            "country_name": created_country.country_name,
            "numeric_code": created_country.numeric_code,
            "capital_city": created_country.capital_city,
            "population": created_country.population,
            "area": created_country.area
        }

    def get_all_countries(self) -> List[Dict]:
        countries = self._get_country_usecase.get_all()
        return [
            {
                "country_id": country.country_id,
                "country_name": country.country_name,
                "numeric_code": country.numeric_code,
                "capital_city": country.capital_city,
                "population": country.population,
                "area": country.area
            }
            for country in countries
        ]

    def get_country_by_id(self, country_id: int) -> Dict:
        country = self._get_country_usecase.get_by_id(country_id)
        return {
            "country_id": country.country_id,
            "country_name": country.country_name,
            "numeric_code": country.numeric_code,
            "capital_city": country.capital_city,
            "population": country.population,
            "area": country.area
        }