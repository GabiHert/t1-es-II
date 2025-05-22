class CurrencyEntity:
    def __init__(self, currency_code: str, currency_name: str, currency_symbol: str, country_id: int):
        self.currency_code = currency_code
        self.currency_name = currency_name
        self.currency_symbol = currency_symbol
        self.country_id = country_id

    def __repr__(self):
        return (
            f"CurrencyEntity(currency_code={self.currency_code!r}, currency_name={self.currency_name!r}, "
            f"currency_symbol={self.currency_symbol!r}, country_id={self.country_id})"
        )