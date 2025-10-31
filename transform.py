# transform.py
import pandas as pd
from typing import Tuple


def transform_movies(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforms raw movie data.
    Cleans, formats, and selects relevant columns.

    Returns a new DataFrame (does not mutate input).
    """
    # Work on a copy to avoid chained-assignment warnings
    df = df.copy()

    # Select essential columns (if missing columns, raise meaningful error)
    required = ['id', 'title', 'release_date', 'vote_average', 'vote_count', 'popularity', 'original_language']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns for transform: {missing}")

    df = df[required].copy()

    # Convert release_date to datetime
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    # Handle missing values (assign back to avoid inplace on slice)
    df['vote_average'] = df['vote_average'].fillna(0)
    df['vote_count'] = df['vote_count'].fillna(0)
    df['popularity'] = df['popularity'].fillna(0)

    # Remove duplicates
    df = df.drop_duplicates(subset='id')

    # Filter invalid rows (optional)
    df = df[df['release_date'].notna()]

    print(f"✅ Transformed Data: {df.shape[0]} clean records ready for loading")
    return df


def validate_schema(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Simple validation helper that ensures output types are reasonable.
    Returns (is_valid, message)
    """
    if df.empty:
        return False, "DataFrame is empty"
    if not pd.api.types.is_datetime64_any_dtype(df['release_date']):
        return False, "release_date is not datetime"
    return True, "ok"
