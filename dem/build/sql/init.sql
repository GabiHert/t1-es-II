CREATE TABLE countries (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR NOT NULL,
    numeric_code INTEGER NOT NULL,
    capital_city VARCHAR NOT NULL,
    population BIGINT NOT NULL,
    area FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE currencies (
    currency_id SERIAL PRIMARY KEY,
    currency_code VARCHAR NOT NULL,
    currency_name VARCHAR NOT NULL,
    currency_symbol VARCHAR NOT NULL,
    country_id INTEGER NOT NULL REFERENCES countries(country_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
); 