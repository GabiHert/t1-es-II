from typing import Dict, List

from application import (
    CountryEntity,
    MissingFieldError,
    InvalidFieldError,
    CountryNotFoundError,
    CreateCountryUseCase,
    GetCountryUseCase,
    DeleteCountryUseCase,
    UpdateCountryUseCase
)


class CountryController:
    def __init__(
        self,
        create_country_usecase: CreateCountryUseCase,
        get_country_usecase: GetCountryUseCase,
        delete_country_usecase: DeleteCountryUseCase,
        update_country_usecase: UpdateCountryUseCase
    ):
        self._create_country_usecase = create_country_usecase
        self._get_country_usecase = get_country_usecase
        self._delete_country_usecase = delete_country_usecase
        self._update_country_usecase = update_country_usecase

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
            "area": created_country.area,
            "created_at": created_country.created_at.isoformat() if created_country.created_at else None,
            "updated_at": created_country.updated_at.isoformat() if created_country.updated_at else None
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
                "area": country.area,
                "created_at": country.created_at.isoformat() if country.created_at else None,
                "updated_at": country.updated_at.isoformat() if country.updated_at else None
            }
            for country in countries
        ]

    def get_country_by_id(self, country_id: int) -> Dict:
        try:
            country = self._get_country_usecase.get_by_id(country_id)
            return {
                "country_id": country.country_id,
                "country_name": country.country_name,
                "numeric_code": country.numeric_code,
                "capital_city": country.capital_city,
                "population": country.population,
                "area": country.area,
                "created_at": country.created_at.isoformat() if country.created_at else None,
                "updated_at": country.updated_at.isoformat() if country.updated_at else None
            }
        except ValueError as e:
            if "Country with id" in str(e) and "not found" in str(e):
                raise CountryNotFoundError(str(e))
            raise InvalidFieldError(str(e))

    def get_country_by_numeric_code(self, numeric_code: int) -> Dict:
        try:
            country = self._get_country_usecase.get_by_numeric_code(numeric_code)
            return {
                "country_id": country.country_id,
                "country_name": country.country_name,
                "numeric_code": country.numeric_code,
                "capital_city": country.capital_city,
                "population": country.population,
                "area": country.area,
                "created_at": country.created_at.isoformat() if country.created_at else None,
                "updated_at": country.updated_at.isoformat() if country.updated_at else None
            }
        except ValueError as e:
            if "Country with numeric code" in str(e) and "not found" in str(e):
                raise CountryNotFoundError(str(e))
            raise InvalidFieldError(str(e))

    def delete_country(self, country_id: int) -> None:
        try:
            self._delete_country_usecase.delete(country_id)
        except ValueError as e:
            if "Country with id" in str(e) and "not found" in str(e):
                raise CountryNotFoundError(str(e))
            raise InvalidFieldError(str(e))

    def update_country(self, country_id: int, country_data: Dict) -> Dict:
        try:
            # Create a CountryEntity with only the fields that are provided
            country_entity = CountryEntity(
                country_name=country_data.get("country_name"),
                numeric_code=country_data.get("numeric_code"),
                capital_city=country_data.get("capital_city"),
                population=country_data.get("population"),
                area=country_data.get("area")
            )
        except ValueError as e:
            raise InvalidFieldError(str(e))

        try:
            updated_country = self._update_country_usecase.update(country_id, country_entity)
            return {
                "country_id": updated_country.country_id,
                "country_name": updated_country.country_name,
                "numeric_code": updated_country.numeric_code,
                "capital_city": updated_country.capital_city,
                "population": updated_country.population,
                "area": updated_country.area,
                "created_at": updated_country.created_at.isoformat() if updated_country.created_at else None,
                "updated_at": updated_country.updated_at.isoformat() if updated_country.updated_at else None
            }
        except ValueError as e:
            if "Country with id" in str(e) and "not found" in str(e):
                raise CountryNotFoundError(str(e))
            raise InvalidFieldError(str(e))

# Create a default instance for Flask routes
country_controller = CountryController(None, None, None, None)  # Will be properly initialized by the injector