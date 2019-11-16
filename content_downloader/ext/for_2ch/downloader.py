import aiohttp
import asyncio
import aiofiles
from content_downloader import config

# I don't know what to do with ClientPayloadError so I decided to use try/except. If ClientPayloadError appears
# the file will be downloaded again


class Downloader:
    _root_url: str = config.config['2CH']['root_url']

    def __init__(self, tread_url, path_to_downloaded_content):
        self._not_loaded_files: list = []
        self._tread_url: str = tread_url
        self._path_to_downloaded_content = path_to_downloaded_content

    async def _download(self, session, file: dict):
        async with session.get(self._root_url + file['path']) as resp_with_file:
            if resp_with_file.status == 200:
                async with aiofiles.open(self._path_to_downloaded_content + '/' + file['name'], 'wb') as f:
                    try:
                        await f.write(await resp_with_file.read())
                    except aiohttp.ClientPayloadError:
                        self._not_loaded_files.append(file)

    async def _get_posts_from_thread(self, session):
        async with session.get(self._tread_url) as resp_with_json:
            if resp_with_json.status == 200:
                return (await resp_with_json.json())['threads'][0]['posts']

    async def download_content_from_thread(self):
        async with aiohttp.ClientSession() as session:
            posts = await self._get_posts_from_thread(session)
            if not posts:
                return None
            tasks = [asyncio.create_task(self._download(session, file)) for post in posts for file in post.get('files', [])]
            await asyncio.gather(*tasks)
            while self._not_loaded_files:
                tasks = [asyncio.create_task(self._download(session, file)) for file in self._not_loaded_files]
                self._not_loaded_files = []
                await asyncio.gather(*tasks)
