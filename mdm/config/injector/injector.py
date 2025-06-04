from application.usecase.create_country import CreateCountryUseCase
from application.usecase.get_country import GetCountryUseCase
from application.usecase.delete_country import DeleteCountryUseCase
from application.usecase.update_country import UpdateCountryUseCase
from application.usecase.create_currency import CreateCurrencyUseCase
from application.usecase.get_currency import GetCurrencyUseCase
from application.usecase.delete_currency import DeleteCurrencyUseCase
from application.usecase.update_currency import UpdateCurrencyUseCase
from application.usecase.sync_data import SyncDataUseCase
from config.db.db import SessionMaker
from infra.entrypoint.controllers.country_controller import CountryController
from infra.entrypoint.controllers.currency_controller import CurrencyController
from infra.entrypoint.controllers.sync_controller import SyncController
from infra.repository.country import CountryRepository
from infra.repository.currency import CurrencyRepository


class Injector:
    def __init__(self):
        self._session = SessionMaker()
        
        # Country dependencies
        self._country_repository = CountryRepository(self._session)
        self._create_country_usecase: CreateCountryUseCase = self._country_repository
        self._get_country_usecase: GetCountryUseCase = self._country_repository
        self._delete_country_usecase: DeleteCountryUseCase = self._country_repository
        self._update_country_usecase: UpdateCountryUseCase = self._country_repository
        self.country_controller = CountryController(
            self._create_country_usecase,
            self._get_country_usecase,
            self._delete_country_usecase,
            self._update_country_usecase
        )
        
        # Currency dependencies
        self._currency_repository = CurrencyRepository(self._session)
        self._create_currency_usecase: CreateCurrencyUseCase = self._currency_repository
        self._get_currency_usecase: GetCurrencyUseCase = self._currency_repository
        self._delete_currency_usecase: DeleteCurrencyUseCase = self._currency_repository
        self._update_currency_usecase: UpdateCurrencyUseCase = self._currency_repository
        self.currency_controller = CurrencyController(
            self._create_currency_usecase,
            self._get_currency_usecase,
            self._delete_currency_usecase,
            self._update_currency_usecase
        )

        # Sync dependencies
        self._sync_data_usecase = SyncDataUseCase()
        self.sync_controller = SyncController(self._sync_data_usecase)


injector = Injector()