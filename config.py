# config.py
# 🔧 Configuration file for API and Database
#
# This file reads configuration from environment variables when available
# and provides sensible defaults. Prefer setting the TMDB API key in
# the environment as TMDB_API_KEY to avoid checking secrets into source.

import os

# TMDB API
API_KEY = os.getenv("TMDB_API_KEY", "YOUR_TMDB_API_KEY")  # set TMDB_API_KEY in env for production
BASE_URL = "https://api.themoviedb.org/3/movie/popular"

# Database configuration
# Supported DB_TYPE values: 'sqlite', 'mysql', 'postgresql'
DB_TYPE = os.getenv("DB_TYPE", "sqlite")
DB_HOST = os.getenv("DB_HOST", "")
DB_NAME = os.getenv("DB_NAME", "moviesdb")
DB_USER = os.getenv("DB_USER", "")
DB_PASS = os.getenv("DB_PASS", "")
DB_PORT = os.getenv("DB_PORT", "")
# Path for sqlite database file when DB_TYPE=sqlite
SQLITE_PATH = os.getenv("SQLITE_PATH", "movies.db")
