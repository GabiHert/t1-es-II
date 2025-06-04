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

1. Clone the repository and navigate to the project root:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Build and start all services:
```bash
# For DEM service
cd dem
make docker_build
make docker_up

# For MDM service
cd ../mdm
make docker_build
make docker_up
```

3. Stop the services:
```bash
# In each service directory
make docker_down
```

Additional commands:
- `make docker_logs`: View service logs
- `make docker_clean`: Clean up everything, including volumes

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
- extractions: Stores extraction metadata and status
  - extraction_id (PK)
  - source
  - status
  - created_at
  - completed_at
  - file_path
  - error
- loads: Stores load process information
  - load_id (PK)
  - service
  - extraction_id (FK)
  - status
  - created_at
  - completed_at
  - error

### MDM Database
- countries: Stores country information
  - country_id (PK)
  - country_name
  - numeric_code
  - capital_city
  - population
  - area
  - created_at
  - updated_at
- currencies: Stores currency information
  - currency_id (PK)
  - currency_code
  - currency_name
  - currency_symbol
  - country_id (FK)
  - created_at
  - updated_at

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