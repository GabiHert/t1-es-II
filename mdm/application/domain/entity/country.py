class CountryEntity:
    def __init__(self, country_name: str, numeric_code: int, capital_city: str, population: int, area: float, country_id: int = None):
        self.country_id = country_id
        self.country_name = country_name
        self.numeric_code = numeric_code
        self.capital_city = capital_city
        self.population = population
        self.area = area

    def __repr__(self):
        return (
            f"Country(country_id={self.country_id}, country_name={self.country_name!r}, numeric_code={self.numeric_code}, "
            f"capital_city={self.capital_city!r}, population={self.population}, area={self.area})"
        )