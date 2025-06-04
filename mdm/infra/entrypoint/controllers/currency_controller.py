from typing import Dict, List

from application import (
    CurrencyEntity,
    MissingFieldError,
    InvalidFieldError,
    CreateCurrencyUseCase,
    GetCurrencyUseCase,
    DeleteCurrencyUseCase,
    UpdateCurrencyUseCase,
    NotFoundError
)


class CurrencyController:
    def __init__(
        self,
        create_currency_usecase: CreateCurrencyUseCase,
        get_currency_usecase: GetCurrencyUseCase,
        delete_currency_usecase: DeleteCurrencyUseCase,
        update_currency_usecase: UpdateCurrencyUseCase
    ):
        self._create_currency_usecase = create_currency_usecase
        self._get_currency_usecase = get_currency_usecase
        self._delete_currency_usecase = delete_currency_usecase
        self._update_currency_usecase = update_currency_usecase

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

    def delete_currency(self, currency_id: int) -> None:
        try:
            self._delete_currency_usecase.delete(currency_id)
        except ValueError as e:
            if "Currency with id" in str(e) and "not found" in str(e):
                raise NotFoundError(str(e))
            raise InvalidFieldError(str(e))

    def update_currency(self, currency_id: int, currency_data: Dict) -> Dict:
        try:
            # Only include fields that are actually present in the update data
            entity_args = {}
            if "currency_code" in currency_data:
                entity_args["currency_code"] = currency_data["currency_code"]
            if "currency_name" in currency_data:
                entity_args["currency_name"] = currency_data["currency_name"]
            if "currency_symbol" in currency_data:
                entity_args["currency_symbol"] = currency_data["currency_symbol"]
            if "country_id" in currency_data:
                entity_args["country_id"] = currency_data["country_id"]
            if "created_at" in currency_data:
                entity_args["created_at"] = currency_data["created_at"]
            if "updated_at" in currency_data:
                entity_args["updated_at"] = currency_data["updated_at"]

            # Create a CurrencyEntity with only the fields that need to be updated
            currency_entity = CurrencyEntity(**entity_args)
        except ValueError as e:
            raise InvalidFieldError(str(e))

        try:
            updated_currency = self._update_currency_usecase.update(currency_id, currency_entity)
            return {
                "currency_id": updated_currency.currency_id,
                "currency_code": updated_currency.currency_code,
                "currency_name": updated_currency.currency_name,
                "currency_symbol": updated_currency.currency_symbol,
                "country_id": updated_currency.country_id,
                "created_at": updated_currency.created_at.isoformat() if updated_currency.created_at else None,
                "updated_at": updated_currency.updated_at.isoformat() if updated_currency.updated_at else None
            }
        except ValueError as e:
            if "Currency with id" in str(e) and "not found" in str(e):
                raise NotFoundError(str(e))
            raise InvalidFieldError(str(e))

# Create a default instance for Flask routes
currency_controller = CurrencyController(None, None, None, None)  # Will be properly initialized by the injector 