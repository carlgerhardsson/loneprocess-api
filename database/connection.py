"""
Database connection and utility functions for Löneprocess API v3.0
"""
import sqlite3
from contextlib import contextmanager
from config import DB_NAME


@contextmanager
def get_db():
    """Database connection context manager"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def dict_from_row(row):
    """Convert sqlite3.Row to dict"""
    if row is None:
        return None
    return {key: row[key] for key in row.keys()}


def init_database():
    """
    Initialize database with all tables and sample data.
    This is called on application startup.
    """
    from .models import create_all_tables, insert_sample_data
    
    create_all_tables()
    insert_sample_data()
    
    print("✓ Database initialized successfully with v3.0 schema")
