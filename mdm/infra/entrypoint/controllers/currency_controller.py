from typing import Dict, List

from application import (
    CurrencyEntity,
    MissingFieldError,
    InvalidFieldError,
    CreateCurrencyUseCase,
    GetCurrencyUseCase
)


class CurrencyController:
    def __init__(
        self,
        create_currency_usecase: CreateCurrencyUseCase,
        get_currency_usecase: GetCurrencyUseCase
    ):
        self._create_currency_usecase = create_currency_usecase
        self._get_currency_usecase = get_currency_usecase

    def create_currency(self, currency_data: Dict) -> Dict:
        required_fields = ["currency_code", "currency_name", "currency_symbol", "country_id"]
        for field in required_fields:
            if field not in currency_data:
                raise MissingFieldError(f"The field '{field}' is required")

        try:
            currency_entity = CurrencyEntity(
                currency_code=currency_data["currency_code"],
                currency_name=currency_data["currency_name"],
                currency_symbol=currency_data["currency_symbol"],
                country_id=currency_data["country_id"]
            )
        except ValueError as e:
            raise InvalidFieldError(str(e))

        created_currency = self._create_currency_usecase.create(currency_entity)
        return {
            "currency_id": created_currency.currency_id,
            "currency_code": created_currency.currency_code,
            "currency_name": created_currency.currency_name,
            "currency_symbol": created_currency.currency_symbol,
            "country_id": created_currency.country_id,
            "created_at": created_currency.created_at.isoformat() if created_currency.created_at else None,
            "updated_at": created_currency.updated_at.isoformat() if created_currency.updated_at else None
        }

    def get_all_currencies(self) -> List[Dict]:
        currencies = self._get_currency_usecase.get_all()
        return [
            {
                "currency_id": currency.currency_id,
                "currency_code": currency.currency_code,
                "currency_name": currency.currency_name,
                "currency_symbol": currency.currency_symbol,
                "country_id": currency.country_id,
                "created_at": currency.created_at.isoformat() if currency.created_at else None,
                "updated_at": currency.updated_at.isoformat() if currency.updated_at else None
            }
            for currency in currencies
        ]

    def get_currency_by_id(self, currency_id: int) -> Dict:
        currency = self._get_currency_usecase.get_by_id(currency_id)
        return {
            "currency_id": currency.currency_id,
            "currency_code": currency.currency_code,
            "currency_name": currency.currency_name,
            "currency_symbol": currency.currency_symbol,
            "country_id": currency.country_id,
            "created_at": currency.created_at.isoformat() if currency.created_at else None,
            "updated_at": currency.updated_at.isoformat() if currency.updated_at else None
        }

    def get_currency_by_code(self, currency_code: str) -> Dict:
        currency = self._get_currency_usecase.get_by_code(currency_code)
        return {
            "currency_id": currency.currency_id,
            "currency_code": currency.currency_code,
            "currency_name": currency.currency_name,
            "currency_symbol": currency.currency_symbol,
            "country_id": currency.country_id,
            "created_at": currency.created_at.isoformat() if currency.created_at else None,
            "updated_at": currency.updated_at.isoformat() if currency.updated_at else None
        }

# Create a default instance for Flask routes
currency_controller = CurrencyController(None, None)  # Will be properly initialized by the injector 