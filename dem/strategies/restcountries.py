import json
import os
from datetime import datetime
import requests

class RestCountriesStrategy:
    SOURCE = "restcountries"
    API_URL = "https://restcountries.com/v3.1/all"
    
    @staticmethod
    def extract(extraction_id):
        response = requests.get(RestCountriesStrategy.API_URL)
        response.raise_for_status()
        data = response.json()
        
        # Create extractions directory if it doesn't exist
        os.makedirs(f"extractions/{RestCountriesStrategy.SOURCE}", exist_ok=True)
        
        # Save data to file
        filename = f"{extraction_id}.json"
        filepath = f"extractions/{RestCountriesStrategy.SOURCE}/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump(data, f)
            
        return filepath

    @staticmethod
    def transform_for_mdm(data):
        country = {
            "country_name": data["name"]["common"],
            "numeric_code": int(data.get("ccn3", 0)),
            "capital_city": data["capital"][0] if data.get("capital") else "Unknown",
            "population": data.get("population", 0),
            "area": data.get("area", 0.0)
        }
        
        currencies = []
        if data.get("currencies"):
            for code, currency_data in data["currencies"].items():
                currency = {
                    "currency_code": code,
                    "currency_name": currency_data.get("name", ""),
                    "currency_symbol": currency_data.get("symbol", ""),
                }
                currencies.append(currency)
                
        return country, currencies 