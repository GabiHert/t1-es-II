CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS extractions (
    extraction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR NOT NULL
);

CREATE TABLE IF NOT EXISTS loads (
    load_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    extraction_id UUID REFERENCES extractions(extraction_id),
    source VARCHAR NOT NULL,
    service VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR NOT NULL
); 