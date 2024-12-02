import logging

import asyncpg

from settings.settings import get_settings

logger = logging.getLogger(__name__)

CREATE_IMAGES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    query VARCHAR(255) NOT NULL,
    image_url TEXT NOT NULL UNIQUE,
    image_data BYTEA NOT NULL,
    width INT,
    height INT,
    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""
CREATE_INDEX_QUERY_SQL = """
CREATE INDEX IF NOT EXISTS idx_images_query ON images (query);
"""


async def create_tables():
    try:
        logger.info("Starting database schema creation...")
        settings = get_settings()
        print("setting debug dict", settings.dict())
        pool = await asyncpg.create_pool(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            min_size=1,
            max_size=10,
        )

        async with pool.acquire() as connection:
            await connection.execute(CREATE_IMAGES_TABLE_SQL)
            logger.info("Successfully created or verified 'images' table")

            await connection.execute(CREATE_INDEX_QUERY_SQL)
            logger.info("Successfully created or verified index on 'query' field")

        await pool.close()
        logger.info("Closed the database connection pool")
        logger.info("Database schema creation completed successfully")

    except Exception as e:
        logger.exception(f"An error occurred while creating tables: {e}")
        raise
