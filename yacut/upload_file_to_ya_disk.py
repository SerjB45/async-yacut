import asyncio
from urllib.parse import quote

import aiohttp

from . import app

DISK_HOST = app.config.get('DISK_HOST')
DISK_API_VERSION = app.config.get('DISK_API_VERSION')
DISK_URL = f'{DISK_HOST}{DISK_API_VERSION}/disk/resources/'
DISK_TOKEN = app.config.get('DISK_TOKEN')
REQUEST_UPLOAD_URL = f'{DISK_URL}upload'
DOWNLOAD_LINK_URL = f'{DISK_URL}download'
AUTH_HEADERS = {'Authorization': f'OAuth {DISK_TOKEN}'}


async def upload_file_and_get_link(session, file):
    filename = file.filename
    payload = {
        'path': f'app:/{quote(filename)}',  # noqa E231
        'overwrite': 'true'
    }
    file_content = file.read()
    async with session.get(
        REQUEST_UPLOAD_URL,
        headers=AUTH_HEADERS,
        params=payload
    ) as response:
        response.raise_for_status()
        upload_data = await response.json()
        upload_url = upload_data['href']
    async with session.put(
        upload_url,
        data=file_content,
        headers=AUTH_HEADERS
    ) as upload_response:
        upload_response.raise_for_status()
    async with session.get(
        DOWNLOAD_LINK_URL,
        headers=AUTH_HEADERS,
        params={'path': f'app:/{filename}'}  # noqa E231
    ) as download_response:
        download_response.raise_for_status()
        download_data = await download_response.json()
        return {
            'name': filename,
            'url': download_data['href']
        }


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
            file_info = await asyncio.gather(*tasks)
        return file_info
