import pandas as pd
from transform import transform_movies


def test_transform_basic():
    data = [
        {"id": 1, "title": "A", "release_date": "2020-01-01", "vote_average": 7.0, "vote_count": 10, "popularity": 5.0, "original_language": "en"},
        {"id": 1, "title": "A", "release_date": "2020-01-01", "vote_average": 7.0, "vote_count": 10, "popularity": 5.0, "original_language": "en"},
        {"id": 2, "title": "B", "release_date": None, "vote_average": None, "vote_count": None, "popularity": None, "original_language": "en"},
    ]
    df = pd.DataFrame(data)
    out = transform_movies(df)

    # Duplicate removed, row with missing release_date filtered out
    assert out.shape[0] == 1
    assert list(out.columns) == ["id", "title", "release_date", "vote_average", "vote_count", "popularity", "original_language"]
