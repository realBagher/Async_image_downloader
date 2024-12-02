import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import unittest
import asyncio
import asyncpg
import logging
from src.settings.settings import get_settings
from src.infrastructre.make_db import create_tables
import logging



logger = logging.getLogger(__name__)


class TestDatabaseSetup(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Set up the database connection pool and start a transaction before each test."""
        logger.info("Setting up the database connection pool for the test.")
        self.settings = get_settings()
        self.pool = await asyncpg.create_pool(
            user=self.settings.POSTGRES_USER,
            password=self.settings.POSTGRES_PASSWORD,
            database=self.settings.POSTGRES_DB,
            host=self.settings.POSTGRES_HOST,
            port=self.settings.POSTGRES_PORT,
            min_size=1,
            max_size=10,
        )
        self.connection = await self.pool.acquire()
        self.transaction = self.connection.transaction()
        await self.transaction.start()
        logger.info("Transaction started for the test.")

    async def asyncTearDown(self):
        """Roll back the transaction and release the connection after each test."""
        logger.info("Rolling back the transaction and cleaning up the database.")
        await self.transaction.rollback()
        await self.pool.release(self.connection)
        await self.pool.close()
        logger.info("Database connection pool closed after the test.")

    async def test_create_tables(self):
        """Test that the 'images' table is created successfully."""
        logger.info("Testing the creation of the 'images' table.")
        
        await create_tables()

       
        result = await self.connection.fetch(
            "SELECT table_name FROM information_schema.tables WHERE table_name = 'images';"
        )
        logger.info(f"Query result for 'images' table existence: {result}")
        self.assertEqual(len(result), 1, "The 'images' table was not created")
        logger.info("The 'images' table was created successfully.")

    async def test_insert_and_retrieve_data(self):
        """Test inserting and retrieving data from the 'images' table."""
        logger.info("Testing insertion and retrieval of data from the 'images' table.")
        
        await self.connection.execute(
            """
            INSERT INTO images (query, image_url, image_data, width, height)
            VALUES ($1, $2, $3, $4, $5)
            """,
            "test_query",
            "http://example.com/image.jpg",
            b"binarydata",
            100,
            200,
        )
        logger.info("Test data inserted into the 'images' table.")

        
        result = await self.connection.fetch(
            "SELECT query, image_url, width, height FROM images WHERE query = $1;",
            "test_query",
        )
        logger.info(f"Query result for retrieving data: {result}")
        self.assertEqual(
            len(result), 1, "No data was retrieved from the 'images' table"
        )
        self.assertEqual(result[0]["query"], "test_query")
        self.assertEqual(result[0]["image_url"], "http://example.com/image.jpg")
        self.assertEqual(result[0]["width"], 100)
        self.assertEqual(result[0]["height"], 200)
        logger.info(
            "Data retrieved and validated successfully from the 'images' table."
        )


if __name__ == "__main__":

    current_working_directory = os.getcwd()
    print(f"Current Working Directory: {current_working_directory}")

    logger.info("Starting the database test suite.")
    unittest.main()
    logger.info("Database test suite completed.")
