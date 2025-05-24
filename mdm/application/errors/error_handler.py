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


class DatabaseError(APIError):
    status_code = 500
    error_code = "DATABASE_ERROR"
    message = "Database operation failed"


error_mapping: Dict[Type[Exception], Type[APIError]] = {
    KeyError: MissingFieldError,
    ValueError: InvalidFieldError,
    JSONDecodeError: JSONValidationError,
} 