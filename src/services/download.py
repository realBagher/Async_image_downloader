
import logging
import aiohttp
import asyncio

logger = logging.getLogger(__name__)




class DownloadImage:
    def __init__(self, timeout: int = 60):
        self.timeout = timeout

    async def download_image(self, url: str) -> bytes:

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, timeout=self.timeout) as response:
                    if response.status == 200:
                        logger.info(f"Successfully downloaded image from {url}")
                        result = await response.read()
                        return result
                    else:
                        logger.error(
                            f"Failed to download {url}: Status {response.status}"
                        )
            except aiohttp.ClientError as e:
                logger.exception(f"HTTP error occurred while downloading {url}: {e}")
            except asyncio.TimeoutError:
                logger.exception(f"Timeout occurred while downloading {url}")
            except Exception as e:
                logger.exception(
                    f"Unexpected error occurred while downloading {url}: {e}"
                )
                raise
        return b""