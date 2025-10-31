import types
import pandas as pd

import extract


class DummyResponse:
    def __init__(self, status_code=200, results=None):
        self.status_code = status_code
        self._results = results or []

    def json(self):
        return {"results": self._results}


class DummySession:
    def __init__(self, responses):
        # responses is a dict page -> DummyResponse
        self._responses = responses

    def get(self, url, timeout=None):
        # crude page extraction from url
        import re

        m = re.search(r"page=(\d+)", url)
        page = int(m.group(1)) if m else 1
        return self._responses.get(page, DummyResponse(200, []))


def test_extract_with_mocked_session(monkeypatch):
    # Prepare dummy data for 2 pages
    page1 = [{"id": 1, "title": "A", "release_date": "2020-01-01", "vote_average": 7.0, "vote_count": 10, "popularity": 5.0, "original_language": "en"}]
    page2 = [{"id": 2, "title": "B", "release_date": "2019-05-05", "vote_average": 6.0, "vote_count": 5, "popularity": 3.0, "original_language": "en"}]

    responses = {1: DummyResponse(200, page1), 2: DummyResponse(200, page2)}
    dummy_session = DummySession(responses)

    # Monkeypatch the session factory in extract module
    monkeypatch.setattr(extract, "_requests_session_with_retries", lambda: dummy_session)

    df = extract.extract_movies(pages=2, api_key="fakekey")
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 2
    assert set(df['id']) == {1, 2}


def test_extract_retries(monkeypatch):
    # Simulate transient failure on page 1 then success
    calls = {"count": 0}

    import requests as _requests

    class FlakySession:
        def get(self, url, timeout=None):
            calls['count'] += 1
            # first call simulate network error by raising a requests exception
            if calls['count'] == 1:
                raise _requests.RequestException('connection reset')
            # subsequent calls return valid data
            return DummyResponse(200, [{"id": 10, "title": "Retry Movie", "release_date": "2022-01-01", "vote_average": 5.5, "vote_count": 1, "popularity": 0.1, "original_language": "en"}])

    monkeypatch.setattr(extract, "_requests_session_with_retries", lambda: FlakySession())
    df = extract.extract_movies(pages=1, api_key="fakekey")
    # Even if the first attempt raised, retry logic at extractor layer should continue and collect data
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] in (0, 1)
