import logging
from typing import List, Optional

import asyncpg

from settings.settings import Settings
from core.entities import Image


logger = logging.getLogger(__name__)


class DataBaseImageRepository:
    def __init__(self, settings: Settings):
        self.pool: Optional[asyncpg.pool.Pool] = None
        self.settings = settings

    async def connect(self) -> None:
        try:
            self.pool = await asyncpg.create_pool(
                user=self.settings.POSTGRES_USER,
                password=self.settings.POSTGRES_PASSWORD,
                database=self.settings.POSTGRES_DB,
                host=self.settings.POSTGRES_HOST,
                port=self.settings.POSTGRES_PORT,
                min_size=1,
                max_size=10,
            )
            logger.info("Successfully connected to the PostgreSQL database")
        except Exception as e:
            logger.exception(f"Failed to connect to the PostgreSQL database: {e}")
            raise

    async def disconnect(self) -> None:
        if self.pool:
            await self.pool.close()
            logger.info("PostgreSQL connection pool closed")
        else:
            logger.warning("The connection pool was not initialized")

    async def insert_image(self, image: Image) -> None:
        if not self.pool:
            raise ConnectionError("Database connection not established.")

        try:
            async with self.pool.acquire() as connection:
                await connection.execute(
                    """
                    INSERT INTO images(query, image_url, image_data, width, height, downloaded_at)
                    VALUES($1, $2, $3, $4, $5, $6)
                    ON CONFLICT (image_url) DO NOTHING
                """,
                    image.query,
                    image.image_url,
                    image.image_data,
                    image.width,
                    image.height,
                    image.downloaded_at,
                )
            logger.info(f"Inserted image from URL: {image.image_url}")
        except Exception as e:
            logger.exception(f"Failed to insert image {image.image_url}: {e}")
            raise

    async def list_images(self, query: str) -> List[Image]:
        if not self.pool:
            raise ConnectionError("Database connection not established.")

        try:
            async with self.pool.acquire() as connection:
                records = await connection.fetch(
                    """
                    SELECT query, image_url, image_data, width, height, downloaded_at
                    FROM images
                    WHERE query = $1
                """,
                    query,
                )
                images = [
                    Image(
                        query=record["query"],
                        image_url=record["image_url"],
                        image_data=record["image_data"],
                        width=record["width"],
                        height=record["height"],
                        downloaded_at=record["downloaded_at"],
                    )
                    for record in records
                ]
            logger.info(f"Listed {len(images)} images for query: {query}")
            return images
        except Exception as e:
            logger.exception(f"Failed to list images for query {query}: {e}")
            raise
