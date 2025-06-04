from datetime import datetime

class CurrencyEntity:
    def __init__(self, currency_code: str = None, currency_name: str = None, currency_symbol: str = None, 
                 country_id: int = None, currency_id: int = None, created_at: datetime = None, 
                 updated_at: datetime = None):
        self.currency_id = currency_id
        self.currency_code = currency_code
        self.currency_name = currency_name
        self.currency_symbol = currency_symbol
        self.country_id = country_id
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return (
            f"CurrencyEntity(currency_id={self.currency_id}, currency_code={self.currency_code!r}, "
            f"currency_name={self.currency_name!r}, currency_symbol={self.currency_symbol!r}, "
            f"country_id={self.country_id}, created_at={self.created_at}, updated_at={self.updated_at})"
        )