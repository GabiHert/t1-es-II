from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError

from application.errors.error_handler import APIError, DatabaseError, error_mapping


def init_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(error: Exception):
        """Handle all unhandled exceptions"""
        # If it's our custom API error, use it directly
        if isinstance(error, APIError):
            return jsonify(error.to_dict()), error.status_code

        # Map known exceptions to our custom errors
        error_class = error_mapping.get(type(error))
        if error_class:
            if callable(error_class):
                api_error = error_class(error)
            else:
                api_error = error_class(str(error))
            return jsonify(api_error.to_dict()), api_error.status_code

        # Handle SQLAlchemy errors
        if isinstance(error, SQLAlchemyError):
            api_error = DatabaseError(str(error))
            return jsonify(api_error.to_dict()), api_error.status_code

        # Handle unknown errors
        app.logger.error(f"Unhandled error: {str(error)}")
        api_error = APIError("An unexpected error occurred")
        return jsonify(api_error.to_dict()), 500 