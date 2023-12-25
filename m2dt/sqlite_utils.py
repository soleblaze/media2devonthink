import os
import sqlite3
from datetime import datetime


def check_and_open_db(db_name="media2dt.db"):
    """Check if a SQLite database exists. If it does, open it. If not, create and open it."""
    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        conn = create_tables(conn)
        print(f"Database {db_name} created and opened successfully.")
    else:
        conn = sqlite3.connect(db_name)
        print(f"Database {db_name} opened successfully.")
    return conn


def create_tables(conn):
    """Create new tables in the SQLite database."""
    cursor = conn.cursor()

    # Create the 'source' table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS source (
            id STRING PRIMARY KEY,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            last_checked TIMESTAMP
        )
    """
    )

    # Complete the 'entries' table creation
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS entries (
            id STRING,
            added TIMESTAMP,
            created TIMESTAMP,
            processed BOOLEAN,
            source_id STRING,
            FOREIGN KEY(source_id) REFERENCES source(id)
        )
        """
    )

    conn.commit()


def list_tables(conn):
    """List all tables in the SQLite database."""
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name FROM sqlite_master WHERE type='table';
    """
    )

    tables = cursor.fetchall()
    for table in tables:
        print(table[0])


def add_entry(conn, id, created, source_id):
    """Add a new entry to the 'entries' table."""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO entries (id, added, created, processed, source_id)
        VALUES (?, datetime('now'), ?, 0, ?)
        """,
        (id, created, source_id),
    )
    conn.commit()


def add_source(
    conn, channel_id, type="youtube", title=None, last_checked="2000-01-01T00:00:00Z"
):
    """Add a new source to the 'source' table."""
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO source (id, type, title, last_checked)
        VALUES (?, ?, ?, ?)
        """,
        (channel_id, type, title, last_checked),
    )
    conn.commit()


def get_source_info(conn):
    """Fetch information about all sources from the 'source' table."""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, type, title, last_checked
        FROM source
        """
    )
    return cursor.fetchall()


def list_sources():
    """Lists all sources"""
    db_connection = check_and_open_db()
    if db_connection is not None:
        sources = get_source_info(db_connection)
        for source in sources:
            print(
                f"ID: {source[0]}, Type: {source[1]}, Title: {source[2]}, Last Checked: {source[3]}"
            )
    else:
        print("Failed to establish database connection.")


def update_timestamp(conn, channel_id):
    """Update the 'last_checked' timestamp of a source."""
    timestamp = (
        datetime.utcnow().isoformat() + "Z"
    )  # Generate a timestamp in ISO 8601 format
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE source
        SET last_checked = ?
        WHERE id = ?
        """,
        (timestamp, channel_id),
    )
    conn.commit()
