from datetime import datetime

class CountryEntity:
    def __init__(self, country_name: str = None, numeric_code: int = None, capital_city: str = None, 
                 population: int = None, area: float = None, country_id: int = None, 
                 created_at: datetime = None, updated_at: datetime = None):
        self.country_id = country_id
        self.country_name = country_name
        self.numeric_code = numeric_code
        self.capital_city = capital_city
        self.population = population
        self.area = area
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return (
            f"Country(country_id={self.country_id}, country_name={self.country_name!r}, numeric_code={self.numeric_code}, "
            f"capital_city={self.capital_city!r}, population={self.population}, area={self.area}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})"
        )