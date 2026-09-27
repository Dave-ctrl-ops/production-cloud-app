import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv()

MIGRATIONS_DIR = Path("migrations")


def get_connection():
    return psycopg.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
    )


def ensure_migration_table(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                version VARCHAR(255) PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
    connection.commit()


def get_applied_migrations(connection):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT version FROM schema_migrations ORDER BY version"
        )
        return {row[0] for row in cursor.fetchall()}


def run_migrations():
    connection = get_connection()

    try:
        ensure_migration_table(connection)

        applied_migrations = get_applied_migrations(connection)

        migration_files = sorted(MIGRATIONS_DIR.glob("*.sql"))

        for migration_file in migration_files:
            version = migration_file.stem

            if version in applied_migrations:
                print(f"Skipping {migration_file.name} - already applied")
                continue

            print(f"Applying {migration_file.name}")

            sql = migration_file.read_text()

            with connection.cursor() as cursor:
                cursor.execute(sql)
                cursor.execute(
                    """
                    INSERT INTO schema_migrations (version, filename)
                    VALUES (%s, %s)
                    """,
                    (version, migration_file.name),
                )

            connection.commit()

            print(f"Applied {migration_file.name}")

    finally:
        connection.close()


if __name__ == "__main__":
    run_migrations()
