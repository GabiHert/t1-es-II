from typing import Dict, Type
from json.decoder import JSONDecodeError


class APIError(Exception):
    """Base error class for API errors"""
    status_code = 500
    error_code = "INTERNAL_SERVER_ERROR"
    message = "An unexpected error occurred"

    def to_dict(self) -> Dict:
        return {
            "error": {
                "code": self.error_code,
                "message": self.message,
                "details": str(self.args[0]) if self.args else None
            }
        }


class ValidationError(APIError):
    status_code = 400
    error_code = "VALIDATION_ERROR"
    message = "Invalid request data"


class JSONValidationError(ValidationError):
    error_code = "INVALID_JSON"
    message = "Invalid JSON format"


class MissingFieldError(ValidationError):
    error_code = "MISSING_FIELD"
    message = "Required field is missing"


class InvalidFieldError(ValidationError):
    error_code = "INVALID_FIELD"
    message = "Field value is invalid"


class NotFoundError(APIError):
    status_code = 404
    error_code = "NOT_FOUND"
    message = "Resource not found"


class CountryNotFoundError(NotFoundError):
    error_code = "COUNTRY_NOT_FOUND"
    message = "Country not found"


class DatabaseError(APIError):
    status_code = 500
    error_code = "DATABASE_ERROR"
    message = "Database operation failed"


def is_country_not_found_error(error: Exception) -> bool:
    return isinstance(error, ValueError) and "Country with id" in str(error) and "not found" in str(error)


error_mapping: Dict[Type[Exception], Type[APIError]] = {
    KeyError: MissingFieldError,
    ValueError: lambda e: CountryNotFoundError(str(e)) if is_country_not_found_error(e) else InvalidFieldError(str(e)),
    JSONDecodeError: JSONValidationError,
} 