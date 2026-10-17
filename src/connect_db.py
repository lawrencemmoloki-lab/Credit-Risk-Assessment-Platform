# Single source of truth for the database connection. Credentials come from
# a local .env file or Streamlit Cloud secrets, whichever is available.
import os
import urllib.parse

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


def _get_setting(key):
    """Environment variable first (local .env), then Streamlit secrets (Cloud)."""
    value = os.getenv(key)
    if value:
        return value
    try:
        import streamlit as st
        return st.secrets.get(key)
    except Exception:
        return None


DB_HOST = _get_setting("DB_HOST")
DB_NAME = _get_setting("DB_NAME")
DB_USER = _get_setting("DB_USER")
DB_PASSWORD = _get_setting("DB_PASSWORD")
DB_PORT = _get_setting("DB_PORT")

if not all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT]):
    raise RuntimeError(
        "Incomplete database credentials. Provide DB_HOST, DB_NAME, DB_USER, "
        "DB_PASSWORD and DB_PORT via .env (local) or app secrets (Streamlit Cloud)."
    )

encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
DATABASE_URL = f"postgresql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# pool_pre_ping re-checks idle connections, avoiding "server closed the
# connection" errors when Supabase drops them between demo clicks.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

if __name__ == "__main__":
    try:
        with engine.connect():
            print("Connected to Supabase PostgreSQL successfully!")
    except Exception as e:
        print("Connection failed:")
        print(e)