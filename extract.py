# extract.py
import os
import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import API_KEY, BASE_URL


def _requests_session_with_retries(retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


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

    session = _requests_session_with_retries()
    for page in range(1, pages + 1):
        url = f"{BASE_URL}?api_key={key}&language=en-US&page={page}"
        try:
            response = session.get(url, timeout=10)
        except requests.RequestException as e:
            print(f"⚠️ Request error when fetching page {page}: {e}")
            continue
        if response.status_code != 200:
            print(f"⚠️ Warning: TMDB API returned status {response.status_code} for page {page}")
            continue
        data = response.json()
        all_movies.extend(data.get("results", []))

    df = pd.DataFrame(all_movies)
    print(f"✅ Extracted {len(df)} movie records from TMDB")
    return df
