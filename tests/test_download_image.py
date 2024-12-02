import os
import asyncio
import unittest
from src.services.search import GoogleImageSearchEngine

from src.services.download import DownloadImage
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  
        logging.FileHandler("debug_test.log", mode="w"),  
    ],
)

logger = logging.getLogger("test_logger")


class TestGoogleImageSearchEngineWithDownload(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        """Set up resources before each test."""
        self.query = "cats"
        self.max_results = 5
        self.download_directory = "test_images"
        os.makedirs(self.download_directory, exist_ok=True)
        self.engine = GoogleImageSearchEngine()
        self.downloader = DownloadImage()

    async def asyncTearDown(self):
        """Clean up resources after each test."""
       
        for file in os.listdir(self.download_directory):
            file_path = os.path.join(self.download_directory, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(self.download_directory)

    async def test_fetch_and_download_images(self):
        """Test fetching image URLs and downloading images."""
       
        urls = await self.engine.fetch_image_urls(
            query=self.query, max_results=self.max_results
        )
        self.assertIsInstance(urls, list)
        self.assertEqual(len(urls), self.max_results)

       
        for idx, url in enumerate(urls):
            image_data = await self.downloader.download_image(url)
            self.assertIsInstance(image_data, bytes)
            self.assertGreater(len(image_data), 0, f"Image data from {url} is empty.")

          
            file_path = os.path.join(self.download_directory, f"image_{idx + 1}.jpg")
            with open(file_path, "wb") as image_file:
                image_file.write(image_data)

            self.assertTrue(
                os.path.exists(file_path), f"Image file {file_path} does not exist."
            )
            print(f"Downloaded and saved: {file_path}")


if __name__ == "__main__":
   
    if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(unittest.main())
    except Exception as e:
        logger.error(f"An error occurred: {e}")
