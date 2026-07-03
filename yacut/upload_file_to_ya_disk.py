import asyncio

import aiohttp
from . import app

DISK_HOST = app.config.get('DISK_HOST')
DISK_URL = f'{DISK_HOST}/v1/disk/resources/'
DISK_TOKEN = app.config.get('DISK_TOKEN')
DISK_API_VERSION = app.config.get('DISK_API_VERSION')
DISK_URL_UPLOAD = f'{DISK_URL}upload'


async def upload_file_and_get_link(session, file):
    pass


async def async_upload_file_to_yandex_disk(files):
    if files is not None:
        tasks = []
        async with aiohttp.ClientSession() as session:
            for file in files:
                tasks.append(
                    asyncio.ensure_future(
                        upload_file_and_get_link(session, file)
                    )
                )
            urls = await asyncio.gather(*tasks)
        return urls
