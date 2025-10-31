"""
Run a short ETL using sample data (no external API calls). Useful to validate transform+load locally
writes to sqlite 'movies.db' by default.
"""
import os
from pathlib import Path

# Ensure we use sqlite for the test run
os.environ.setdefault("DB_TYPE", "sqlite")

from transform import transform_movies
from load import load_movies
import pandas as pd

sample = [
    {"id": 101, "title": "Sample Movie A", "release_date": "2021-05-01", "vote_average": 8.1, "vote_count": 120, "popularity": 50.2, "original_language": "en"},
    {"id": 102, "title": "Sample Movie B", "release_date": "2020-03-15", "vote_average": 7.0, "vote_count": 80, "popularity": 30.5, "original_language": "en"},
    {"id": 103, "title": "Bad Movie", "release_date": None, "vote_average": None, "vote_count": None, "popularity": None, "original_language": "en"},
]

df = pd.DataFrame(sample)
print("Input sample rows:", df.shape[0])
clean = transform_movies(df)
print("Transformed rows:", clean.shape[0])

# load into default sqlite (movies.db)
load_movies(clean, table_name="movies_sample")
print("✅ Sample ETL run complete. Check movies.db or movies_sample_fallback.csv if fallback occurred.")
