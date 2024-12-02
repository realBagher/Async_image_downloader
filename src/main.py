from settings.settings import Settings
from use_case.use_case import MainImageAggregationControlUseCase

from repositories.postgres import DataBaseImageRepository
from services.download import DownloadImage
from services.search import GoogleImageSearchEngine
from services.processing import ProcessImage

from helper.resize_image import resize_image

import asyncio

from infrastructre.make_db import create_tables

# import asyncio
# from service_infrastructure.infrastrcture_service import GoogleImageSearchEngine
import logging

logger = logging.getLogger("test_logger")

logger.info("This is a test log message!")

settings = Settings(_env_file="./src/.env")

# async def main():
# try:
#     async with GoogleImageSearchEngine() as engine:

#             query = "cats"  # The search query
#             max_results = 8  # The
#             logger.info(
#                 f"Fetching up to {max_results} image URLs for query: '{query}'..."
#             )

#             urls = await engine.fetch_image_urls(query=query, max_results=max_results)
#             print("Fetched Image URLs:")
#             for url in urls:
#                 print(url)
# except Exception as e:
#     logger.exception(f"An error occurred: {e}")


async def wrapper():

    await create_tables()

    repository = DataBaseImageRepository(settings)
    search_service = GoogleImageSearchEngine()
    download_service = DownloadImage()
    process_service = ProcessImage()

    process_service.processing_func = resize_image

    # Pass dependencies to the use case
    controler = MainImageAggregationControlUseCase(
        repository=repository,
        search_service=search_service,
        download_service=download_service,
        process_service=process_service,
    )
    query = input("please enter a search term \t")
    resultNumber = int(input("Please enter number of results \t"))
    await controler.process(query, resultNumber)

    print("Loaded Settings:")
    print(settings.model_dump())


if __name__ == "__main__":

    asyncio.run(wrapper())
