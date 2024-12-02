import asyncio
import logging

from typing import Tuple







logger = logging.getLogger(__name__)


class ProcessImage:
    async def process_image(
        self,
        image_data: bytes,
    ) -> Tuple[bytes, int, int]:

        loop = asyncio.get_event_loop()
        try:
            processed_data, width, height = await loop.run_in_executor(
                None, self.processing_func, image_data
            )
            logger.info(f"Processed image to {width}x{height}")
            return processed_data, width, height
        except Exception as e:
            logger.exception(f"Error processing image: {e}")
            raise