# Data Management System

This system consists of two microservices that work together to manage country and currency data:
- **DEM (Data Extraction and Management)**: Responsible for extracting data from external sources
- **MDM (Master Data Management)**: Manages the master data for countries and currencies

## System Architecture

### DEM Service (Port 5001)
Handles data extraction from external sources and loads it into the MDM service. Features:
- Extracts country and currency data from restcountries.com
- Stores extracted data in JSON format
- Manages extraction and load processes
- Provides API endpoints for data extraction control

### MDM Service (Port 5002)
Manages the master data for countries and currencies. Features:
- CRUD operations for countries and currencies
- Relationship management between countries and currencies
- Data validation and consistency checks
- RESTful API for data access

## Setup

### Prerequisites
- Docker and Docker Compose (recommended)
- Python 3.8+
- PostgreSQL 13+

### Using Docker (Recommended)

1. Start all services:
```bash
make up
```

2. View service logs:
```bash
make logs
```

3. Stop the services:
```bash
make down
```

4. Clean up everything (including volumes):
```bash
make clean
```

### Manual Setup

#### DEM Service
1. Create a PostgreSQL database named `dem`
2. Install dependencies:
```bash
cd dem
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5433/dem
```

4. Run the service:
```bash
python run.py
```

#### MDM Service
1. Create a PostgreSQL database named `mdm`
2. Install dependencies:
```bash
cd mdm
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5432/mdm
```

4. Run the service:
```bash
python run.py
```

## Services and Ports

### DEM Service
- API: http://localhost:5001
- PostgreSQL: localhost:5433
- Swagger Documentation: http://localhost:5001/swagger

### MDM Service
- API: http://localhost:5002
- PostgreSQL: localhost:5432
- Swagger Documentation: http://localhost:5002/swagger

## API Documentation

### DEM API Endpoints

#### Data Extraction
- `GET /source/:source/extractions`: List all extractions for a source
- `POST /source/:source/extraction`: Create new extraction
- `POST /extractions/:extraction_id`: Reprocess an existing extraction

#### Data Loading
- `POST /load`: Create new load process
- `GET /loads`: List all load processes

### MDM API Endpoints

#### Countries
- `GET /countries`: List all countries
- `POST /countries`: Create new country
- `GET /countries/{country_id}`: Get country by ID
- `GET /countries/numeric-code/{numeric_code}`: Get country by numeric code

#### Currencies
- `GET /currencies`: List all currencies
- `POST /currencies`: Create new currency
- `GET /currencies/{currency_id}`: Get currency by ID
- `PUT /currencies/{currency_id}`: Update currency
- `DELETE /currencies/{currency_id}`: Delete currency
- `GET /currencies/code/{code}`: Get currency by code

## Data Flow

1. DEM extracts data from external sources (e.g., restcountries.com)
2. Extracted data is stored in JSON files in `dem/extractions/<source>`
3. Load process transfers data from DEM to MDM
4. MDM stores and manages the data in its database
5. Data can be accessed and managed through MDM's API

## Supported Sources
- restcountries: Extracts country and currency data from restcountries.com

## File Storage
Extracted data is stored in the `extractions/<source>` directory with the following format:
`<extraction_id>_<timestamp>.json`

## Database Schema

### DEM Database
- extractions: Stores extraction metadata
  - extraction_id (UUID, PK): Unique identifier for the extraction
  - source (VARCHAR): Source of the extraction (e.g., restcountries)
  - status (VARCHAR): Current status of the extraction
  - created_at (TIMESTAMP): When the extraction was created

- loads: Stores load process information
  - load_id (UUID, PK): Unique identifier for the load
  - extraction_id (UUID, FK): Reference to the extraction
  - source (VARCHAR): Source of the data
  - service (VARCHAR): Target service (e.g., mdm)
  - created_at (TIMESTAMP): When the load was created
  - status (VARCHAR): Current status of the load

### MDM Database
- countries: Stores country information
  - country_id (SERIAL, PK): Auto-incrementing identifier
  - country_name (VARCHAR): Official name of the country
  - numeric_code (INTEGER): ISO numeric country code
  - capital_city (VARCHAR): Name of the capital city
  - population (BIGINT): Total population
  - area (FLOAT): Total area in square kilometers
  - created_at (TIMESTAMP): When the record was created
  - updated_at (TIMESTAMP): When the record was last modified

- currencies: Stores currency information
  - currency_id (SERIAL, PK): Auto-incrementing identifier
  - currency_code (VARCHAR): ISO currency code
  - currency_name (VARCHAR): Full name of the currency
  - currency_symbol (VARCHAR): Currency symbol
  - country_id (INTEGER, FK): Reference to countries table
  - created_at (TIMESTAMP): When the record was created
  - updated_at (TIMESTAMP): When the record was last modified

## Error Handling
Both services implement consistent error handling:
- 400: Bad Request - Invalid input data
- 404: Not Found - Resource not found
- 500: Internal Server Error - Unexpected errors

## Timestamps
All entities include:
- created_at: When the record was created
- updated_at: When the record was last modified (MDM only)
- completed_at: When a process finished (DEM only) 