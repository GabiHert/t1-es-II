import json
from datetime import datetime
import threading
from infra.repositories.models import Extraction, Load
from application.strategies.restcountries import RestCountriesStrategy
from config.database import db_session
import requests
import logging

log = logging.getLogger(__name__)


class ExtractionService:
    STRATEGIES = {
        "restcountries": RestCountriesStrategy
    }
    
    MDM_BASE_URL = "http://mdm:5002"
    
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
            # Get the extraction record to use its created_at timestamp
            extraction = db_session.query(Extraction).filter_by(extraction_id=load.extraction_id).first()
            if not extraction:
                raise ValueError("Extraction not found")
            
            # Find the latest extraction file
            import glob
            import os
            
            files = glob.glob(f"extractions/{load.source}/{load.extraction_id}.json")
            if not files:
                raise ValueError("Extraction file not found")
                
            latest_file = max(files, key=os.path.getctime)
            
            with open(latest_file, 'r') as f:
                data = json.load(f)
                
            strategy = ExtractionService.STRATEGIES[load.source]
            
            # Process each country
            for country_data in data:
                # Check if country exists using numeric code
                response = requests.get(f"{ExtractionService.MDM_BASE_URL}/countries/numeric/{country_data.get('ccn3', 0)}")
                existing_country = None
                
                if response.status_code == 200:
                    existing_country = response.json()
                    # Get existing currencies for this country
                    currencies_response = requests.get(f"{ExtractionService.MDM_BASE_URL}/currencies")
                    existing_currencies = [c for c in currencies_response.json() 
                                        if c.get("country_id") == existing_country["country_id"]]
                    existing_country["currencies"] = existing_currencies
                
                # Transform data with existing timestamps if available
                country, currencies = strategy.transform_for_mdm(country_data, existing_country)
                
                # Set timestamps based on extraction's created_at
                # country["updated_at"] = extraction.created_at.isoformat()
                # if not existing_country:
                #     country["created_at"] = extraction.created_at.isoformat()
                
                if response.status_code == 404:
                    # Create new country
                    response = requests.post(f"{ExtractionService.MDM_BASE_URL}/countries",
                                          json=country)
                    response.raise_for_status()
                    country_id = response.json()["country_id"]
                else:
                    country_id = existing_country["country_id"]
                    # Only update if extraction is newer than the last update
                    existing_updated_at = datetime.fromisoformat(existing_country["updated_at"].replace('Z', '+00:00'))
                    
                    if extraction.created_at > existing_updated_at:
                        requests.patch(f"{ExtractionService.MDM_BASE_URL}/countries/{country_id}",
                                    json=country)
                
                # Process currencies
                for currency_data in currencies:
                    currency_data["country_id"] = country_id
                    # currency_data["updated_at"] = extraction.created_at.isoformat()
                    
                    response = requests.get(f"{ExtractionService.MDM_BASE_URL}/currencies/code/{currency_data['currency_code']}")
                    
                    if response.status_code == 404:
                        currency_data["created_at"] = extraction.created_at.isoformat()
                        requests.post(f"{ExtractionService.MDM_BASE_URL}/currencies",
                                   json=currency_data)
                    else:
                        existing_currency = response.json()
                        # Only update if extraction is newer than the last update
                        existing_updated_at = datetime.fromisoformat(existing_currency["updated_at"].replace('Z', '+00:00'))
                        
                        if extraction.created_at > existing_updated_at:
                            # Preserve original created_at from existing currency
                            currency_data["created_at"] = existing_currency["created_at"]
                            requests.patch(f"{ExtractionService.MDM_BASE_URL}/currencies/{existing_currency['currency_id']}",
                                       json=currency_data)
            
            load.status = "FINISHED"
            
        except Exception as e:
            load.status = "ERROR"
            log.error(f"Error processing load {load_id}: {str(e)}")
            
        finally:
            db_session.commit() 