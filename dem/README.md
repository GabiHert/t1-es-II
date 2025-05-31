# Data Extraction and Management (DEM) Service

This service is responsible for extracting data from various sources and loading it into the MDM (Master Data Management) service.

## Setup

### Using Docker (Recommended)

1. Build and start the services:
```bash
make docker_build
make docker_up
```

2. Stop the services:
```bash
make docker_down
```

Additional commands:
- `make docker_logs`: View service logs
- `make docker_clean`: Clean up everything, including volumes

### Manual Setup

1. Create a PostgreSQL database named `dem`
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (optional):
```bash
export DATABASE_URL=postgresql://postgres:postgres@localhost:5433/dem
```

4. Run the service:
```bash
python run.py
```

The service will run on port 5001 by default.

## Services

- DEM API: http://localhost:5001
- PostgreSQL: localhost:5433

## API Endpoints

### GET /source/:source/extractions
Returns all extractions for a specific source.

### POST /source/:source/extraction
Creates a new extraction for the specified source.

### POST /load
Creates a new load process.
```json
{
    "service": "mdm",
    "extraction_id": "..."
}
```

### GET /loads
Returns all load processes.

### POST /extractions/:extraction_id
Reprocesses an existing extraction.

## Supported Sources
- restcountries: Extracts country and currency data from restcountries.com

## Supported Services
- mdm: Master Data Management service for countries and currencies

## File Storage
Extracted data is stored in the `extractions/<source>` directory with the following format:
`<extraction_id>_<timestamp>.json` 