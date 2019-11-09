import aiohttp
import asyncio
import aiofiles
from content_downloader import config

# I don't know what to do with ClientPayloadError so I decided to use try/except. If ClientPayloadError appears
# the file will be downloaded again


class Downloader:
    __root_url: str = config.config['2CH']['root_url']
    __download_path: str = config.download_path

    def __init__(self, tread_url):
        self.__not_loaded_files: list = []
        self.__tread_url: str = self._jsonify_url(tread_url)

    def _jsonify_url(self, url):
        return '.'.join(url.split('.')[:-1]) + '.json'

    async def _download(self, session, file: dict):
        async with session.get(self.__root_url + file['path']) as resp_with_file:
            if resp_with_file.status == 200:
                async with aiofiles.open(self.__download_path + file['name'], 'wb') as f:
                    try:
                        await f.write(await resp_with_file.read())
                    except aiohttp.ClientPayloadError:
                        self.__not_loaded_files.append(file)

    async def _get_posts_from_thread(self, session):
        async with session.get(self.__tread_url) as resp_with_json:
            if resp_with_json.status == 200:
                return (await resp_with_json.json())['threads'][0]['posts']

    async def download_content_from_thread(self):
        async with aiohttp.ClientSession() as session:
            posts = await self._get_posts_from_thread(session)
            if not posts:
                return None
            tasks = [asyncio.create_task(self._download(session, file)) for post in posts for file in post.get('files', [])]
            await asyncio.gather(*tasks)
            while self.__not_loaded_files:
                tasks = [asyncio.create_task(self._download(session, file)) for file in self.__not_loaded_files]
                self.__not_loaded_files = []
                await asyncio.gather(*tasks)
