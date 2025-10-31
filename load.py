# load.py
import os
import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from config import DB_TYPE, DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT, SQLITE_PATH


def load_movies(df, table_name="movies", connection_url: str = None):
    """
    Loads the cleaned movie data into a SQL database.
    Supports sqlite (default), MySQL or PostgreSQL. If DB connection fails,
    falls back to writing a CSV file named '<table_name>_fallback.csv'.
    """
    # If caller provides a connection_url, use it (this enables in-memory sqlite for tests)
    if connection_url is None:
        if DB_TYPE == "sqlite":
            connection_url = f"sqlite:///{SQLITE_PATH}"
        elif DB_TYPE == "mysql":
            # Requires pymysql
            connection_url = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        elif DB_TYPE == "postgresql":
            # Requires psycopg2
            connection_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        else:
            print(f"⚠️ Unknown DB_TYPE '{DB_TYPE}', defaulting to sqlite file: {SQLITE_PATH}")
            connection_url = f"sqlite:///{SQLITE_PATH}"

    try:
        engine = sqlalchemy.create_engine(connection_url)
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        print(f"✅ Data successfully loaded into the '{table_name}' table (conn={connection_url}).")
    except SQLAlchemyError as e:
        fallback = f"{table_name}_fallback.csv"
        print("❌ Database load failed:", e)
        print(f"➡️ Falling back to writing CSV: {fallback}")
        df.to_csv(fallback, index=False)
        print(f"✅ Data written to {fallback}")
