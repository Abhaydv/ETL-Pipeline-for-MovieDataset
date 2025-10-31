# extract.py
import os
import requests
import pandas as pd
from config import API_KEY, BASE_URL


def extract_movies(pages=3, api_key=None):
    """
    Extracts movie data from TMDB API.
    Args:
        pages (int): Number of pages to fetch (each page = ~20 movies)
        api_key (str): Optional API key override. If not provided, uses config.API_KEY
    Returns:
        DataFrame: Raw movie data
    """
    key = api_key or API_KEY or os.getenv("TMDB_API_KEY")
    if not key or key == "YOUR_TMDB_API_KEY":
        raise ValueError(
            "TMDB API key not set. Set the TMDB_API_KEY environment variable or update config.API_KEY"
        )

    all_movies = []

    for page in range(1, pages + 1):
        url = f"{BASE_URL}?api_key={key}&language=en-US&page={page}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"⚠️ Warning: TMDB API returned status {response.status_code} for page {page}")
            continue
        data = response.json()
        all_movies.extend(data.get("results", []))

    df = pd.DataFrame(all_movies)
    print(f"✅ Extracted {len(df)} movie records from TMDB")
    return df
