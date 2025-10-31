-- SQL schema for movies table (example)
-- Adjust types for MySQL/Postgres as needed

CREATE TABLE IF NOT EXISTS movies (
    id BIGINT PRIMARY KEY,
    title TEXT,
    release_date DATE,
    vote_average FLOAT,
    vote_count BIGINT,
    popularity FLOAT,
    original_language VARCHAR(8)
);
