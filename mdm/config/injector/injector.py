from application.usecase.create_country import CreateCountryUseCase
from application.usecase.get_country import GetCountryUseCase
# from application.usecase.create_currency import CreateCurrencyUseCase
from config.db.db import SessionMaker
from infra.entrypoint.controllers.country_controller import CountryController
from infra.repository.country import CountryRepository


class Injector:
    def __init__(self):
        self._session = SessionMaker()
        self._country_repository = CountryRepository(self._session)
        self._create_country_usecase: CreateCountryUseCase = self._country_repository
        self._get_country_usecase: GetCountryUseCase = self._country_repository
        self.country_controller = CountryController(
            self._create_country_usecase,
            self._get_country_usecase
        )

injector = Injector()