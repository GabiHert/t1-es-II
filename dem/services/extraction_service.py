import json
from datetime import datetime
import threading
from models import Extraction, Load
from strategies.restcountries import RestCountriesStrategy
from config.database import db_session
import requests

class ExtractionService:
    STRATEGIES = {
        "restcountries": RestCountriesStrategy
    }
    
    MDM_BASE_URL = "http://localhost:8080"
    
    @staticmethod
    def get_extractions_by_source(source):
        return db_session.query(Extraction).filter_by(source=source).all()
    
    @staticmethod
    def create_extraction(source):
        if source not in ExtractionService.STRATEGIES:
            raise ValueError(f"Unsupported source: {source}")
            
        extraction = Extraction(source=source, status="PENDING")
        db_session.add(extraction)
        db_session.commit()
        
        try:
            strategy = ExtractionService.STRATEGIES[source]
            filepath = strategy.extract(extraction.extraction_id)
            extraction.status = "FINISHED"
        except Exception as e:
            extraction.status = "ERROR"
            raise e
        finally:
            db_session.commit()
            
        return extraction
    
    @staticmethod
    def create_load(service, extraction_id):
        extraction = db_session.query(Extraction).filter_by(extraction_id=extraction_id).first()
        if not extraction:
            raise ValueError("Extraction not found")
            
        load = Load(
            extraction_id=extraction_id,
            service=service,
            source=extraction.source,
            status="PENDING"
        )
        db_session.add(load)
        db_session.commit()
        
        # Start background process
        thread = threading.Thread(
            target=ExtractionService._process_load,
            args=(load.load_id,)
        )
        thread.start()
        
        return load
    
    @staticmethod
    def get_all_loads():
        return db_session.query(Load).all()
    
    @staticmethod
    def reprocess_extraction(extraction_id):
        extraction = db_session.query(Extraction).filter_by(extraction_id=extraction_id).first()
        if not extraction:
            raise ValueError("Extraction not found")
            
        # Create a new load for reprocessing
        load = Load(
            extraction_id=extraction_id,
            service="mdm",
            source=extraction.source,
            status="PENDING"
        )
        db_session.add(load)
        db_session.commit()
        
        # Start background process
        thread = threading.Thread(
            target=ExtractionService._process_load,
            args=(load.load_id,)
        )
        thread.start()
        
        return load
    
    @staticmethod
    def _process_load(load_id):
        load = db_session.query(Load).filter_by(load_id=load_id).first()
        if not load:
            return
            
        try:
            # Find the latest extraction file
            import glob
            import os
            
            files = glob.glob(f"extractions/{load.source}/{load.extraction_id}.json")
            if not files:
                raise ValueError("Extraction file not found")
                
            latest_file = max(files, key=os.path.getctime)
            # Get file timestamp once, will be used for all comparisons
            file_timestamp = datetime.fromtimestamp(os.path.getctime(latest_file))
            
            with open(latest_file, 'r') as f:
                data = json.load(f)
                
            strategy = ExtractionService.STRATEGIES[load.source]
            
            # Process each country
            for country_data in data:
                country, currencies = strategy.transform_for_mdm(country_data)
                
                # Check if country exists
                response = requests.get(f"{ExtractionService.MDM_BASE_URL}/countries/{country['numeric_code']}")
                
                if response.status_code == 404:
                    # Create new country
                    response = requests.post(f"{ExtractionService.MDM_BASE_URL}/countries",
                                          json=country)
                    response.raise_for_status()
                    country_id = response.json()["country_id"]
                else:
                    existing_country = response.json()
                    country_id = existing_country["country_id"]
                    
                    # Update if our data is newer
                    country_updated_at = datetime.fromisoformat(existing_country["updated_at"])
                    
                    if file_timestamp > country_updated_at:
                        requests.patch(f"{ExtractionService.MDM_BASE_URL}/countries/{country_id}",
                                    json=country)
                
                # Process currencies
                for currency_data in currencies:
                    currency_data["country_id"] = country_id
                    
                    response = requests.get(f"{ExtractionService.MDM_BASE_URL}/currencies/code/{currency_data['currency_code']}")
                    
                    if response.status_code == 404:
                        requests.post(f"{ExtractionService.MDM_BASE_URL}/currencies",
                                   json=currency_data)
                    else:
                        existing_currency = response.json()
                        currency_updated_at = datetime.fromisoformat(existing_currency["updated_at"])
                        
                        if file_timestamp > currency_updated_at:
                            requests.patch(f"{ExtractionService.MDM_BASE_URL}/currencies/{existing_currency['currency_id']}",
                                       json=currency_data)
            
            load.status = "FINISHED"
            
        except Exception as e:
            load.status = "ERROR"
            print(f"Error processing load {load_id}: {str(e)}")
            
        finally:
            db_session.commit() 