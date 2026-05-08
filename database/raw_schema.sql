CREATE TABLE IF NOT EXISTS github_raw (
    id SERIAL PRIMARY KEY,
    endpoint TEXT,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payload JSONB
);

CREATE TABLE IF NOT EXISTS stackoverflow_raw (
    id SERIAL PRIMARY KEY,
    endpoint TEXT,
    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payload JSONB
);