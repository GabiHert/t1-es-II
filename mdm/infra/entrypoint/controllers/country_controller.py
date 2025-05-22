


from application.usecase.create_country import CreateCountryUseCase
from infra.entrypoint.dtos.country import CountryDto


class CountryController:
    def __init__(self, create_country_usecase: CreateCountryUseCase):
        self.create_country_usecase = create_country_usecase

    def create_country(self, request_data)->CountryDto:
            country_dto = CountryDto(**request_data)
            country_entity = country_dto.to_entity()
            country_entity = self.create_country_usecase.create(country_entity)
            return country_dto.from_entity(country_entity)