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
    def transform_for_mdm(data, existing_data=None):
        current_time = datetime.utcnow().isoformat()
        
        # If we have existing data, use its created_at, otherwise use current time
        created_at = existing_data.get("created_at") if existing_data else current_time
        
        country = {
            "country_name": data["name"]["common"],
            "numeric_code": int(data.get("ccn3", 0)),
            "capital_city": data["capital"][0] if data.get("capital") else "Unknown",
            "population": data.get("population", 0),
            "area": data.get("area", 0.0),
            "created_at": created_at,
            "updated_at": current_time
        }
        
        currencies = []
        if data.get("currencies"):
            for code, currency_data in data["currencies"].items():
                # For currencies, if we have existing data for this code, use its created_at
                existing_currency = next((c for c in existing_data.get("currencies", []) 
                                       if c.get("currency_code") == code), None) if existing_data else None
                
                currency = {
                    "currency_code": code,
                    "currency_name": currency_data.get("name", ""),
                    "currency_symbol": currency_data.get("symbol", ""),
                    "created_at": existing_currency.get("created_at") if existing_currency else current_time,
                    "updated_at": current_time
                }
                currencies.append(currency)
                
        return country, currencies 