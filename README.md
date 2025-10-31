# 🎬 ETL Pipeline for Movie Dataset (TMDB)

## 📌 Overview
This project builds an automated ETL (Extract, Transform, Load) pipeline that:
- Fetches popular movie data from TMDB API
- Cleans and transforms the dataset using Pandas
- Loads the processed data into a MySQL/PostgreSQL database

## 🧠 Tech Stack
- **Python**
- **TMDB API**
- **Pandas**
- **SQLAlchemy + MySQL/PostgreSQL**
- (Optional) **Airflow** for automation

## 🧩 Steps to Run
1. Clone this repo  
2. Get a free TMDB API key → [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)  
3. Update credentials in `config.py`  
4. Install dependencies:
   # 🎬 ETL Pipeline for Movie Dataset (TMDB)

   ## Overview
   This project builds a simple ETL pipeline that:
   - Fetches popular movie data from TMDB
   - Cleans and transforms the dataset using pandas
   - Loads the processed data into a SQL database (sqlite/mysql/postgres) or falls back to CSV

   ## Quick start (Windows PowerShell)

   1. Install dependencies (use a virtual environment):

   ```powershell
   python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
   ```

   2. Set your TMDB API key in the environment (replace KEY):

   ```powershell
   $env:TMDB_API_KEY = 'YOUR_REAL_KEY'
   ```

   3. Run the pipeline (default uses sqlite 'movies.db'):

   ```powershell
   python etl_pipeline.py --pages 3
   ```

   ## Docker

   Build and run with Docker (creates a container that runs the pipeline):

   ```powershell
   docker build -t movies-etl .
   docker run --rm movies-etl
   ```

   ## Database schema

   An example SQL schema is available at `sql/create_movies_table.sql` — use it to create the target table in your DB before running the pipeline into MySQL/Postgres if you prefer explicit schema management.

   4. To load into MySQL or PostgreSQL, set DB_TYPE and other DB_* environment vars before running:

   ```powershell
   $env:DB_TYPE='mysql'; $env:DB_HOST='localhost'; $env:DB_USER='root'; $env:DB_PASS='pw'; $env:DB_NAME='moviesdb'; $env:DB_PORT='3306'
   python etl_pipeline.py --pages 3
   ```

   5. If DB load fails, the pipeline will write a fallback CSV named `movies_fallback.csv`.

   ## Development

   - Small unit tests included (pytest). Run with:

   ```powershell
   pytest -q
   ```

   ## Notes
   - Keep your TMDB API key secret. Prefer using environment variables over editing `config.py`.
   - The default DB for quick experiments is sqlite (file `movies.db`).

