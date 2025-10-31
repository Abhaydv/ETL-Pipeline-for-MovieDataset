# etl_pipeline.py
import argparse
import sys
import logging
from extract import extract_movies
from transform import transform_movies
from load import load_movies


def _setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def run_etl(pages=3, table_name="movies"):
    logging.info("🚀 Starting ETL Pipeline...")

    logging.info("Step 1: Extracting Data from TMDB API...")
    raw_df = extract_movies(pages=pages)

    logging.info("Step 2: Transforming Data...")
    clean_df = transform_movies(raw_df)

    logging.info("Step 3: Loading Data into Database or fallback...")
    load_movies(clean_df, table_name=table_name)

    logging.info("🎉 ETL Pipeline Completed Successfully!")


def _cli(argv=None):
    _setup_logging()
    parser = argparse.ArgumentParser(description="Run ETL pipeline for TMDB popular movies")
    parser.add_argument("--pages", type=int, default=3, help="Number of pages to fetch (default: 3)")
    parser.add_argument("--table", type=str, default="movies", help="DB table name to load into")
    parser.add_argument("--db-type", type=str, default=None, help="Optional override for DB_TYPE (sqlite/mysql/postgresql)")
    args = parser.parse_args(argv)

    # Allow temporary override of DB_TYPE via CLI
    if args.db_type:
        import os as _os

        _os.environ["DB_TYPE"] = args.db_type

    try:
        run_etl(pages=args.pages, table_name=args.table)
    except Exception as e:
        logging.exception("ETL failed")
        sys.exit(1)


if __name__ == "__main__":
    _cli()
