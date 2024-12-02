import asyncio
import logging

import aiohttp
from typing import Tuple


from typing import List


from settings.settings import get_settings

# search engine
from aiohttp import ClientSession

logger = logging.getLogger(__name__)



class GoogleImageSearchEngine:
    BASE_URL = "https://www.googleapis.com/customsearch/v1"

    def __init__(self):
        self.settings = get_settings()

    async def fetch_image_urls(self, query: str, max_results: int) -> List[str]:
        image_urls: List[str] = []
        start = 1
        per_page = 10

        async with aiohttp.ClientSession() as session:
            while len(image_urls) < max_results:
                params = {
                    "key": self.settings.API_KEY,
                    "cx": self.settings.SEARCH_ENGINE_ID,
                    "q": query,
                    "searchType": "image",
                    "start": start,
                    "num": min(per_page, max_results - len(image_urls)),
                }
                try:
                    async with session.get(self.BASE_URL, params=params) as result:
                        if result.status != 200:
                            logger.error(f"Error fetching image URLs: {result.status}")
                            result.raise_for_status()
                        data = await result.json()
                        items = data.get("items", [])
                        if not items:
                            logger.info("No more images found")
                            break
                        fetched_urls = [
                            item["link"] for item in items if "link" in item
                        ]
                        image_urls.extend(fetched_urls)
                        logger.info(f"Fetched {len(fetched_urls)} image URLs")
                        start += per_page

                except aiohttp.ClientError as e:
                    logger.exception(f"HTTP error occurred: {e}")
                    raise
                except Exception as e:
                    logger.exception(f"Unexpected error occurred: {e}")
                    raise

        return image_urls[:max_results]
