import aiohttp
import asyncio
import aiofiles
from content_downloader import config


class Downloader:
    __root_url = config.config['2CH']['root_url']
    __download_path = config.download_path

    def __init__(self, tread_url):
        self.__not_loaded_files = []
        self.__tread_url = self.__jsonify_url(tread_url)

    def __jsonify_url(self, url):
        return '.'.join(url.split('.')[:-1]) + '.json'

    async def __download(self, session, file):
        async with session.get(self.__root_url + file['path']) as resp_with_file:
            if resp_with_file.status == 200:
                async with aiofiles.open(self.__download_path + file['name'], 'wb') as f:
                    try:
                        await f.write(await resp_with_file.read())
                    except aiohttp.ClientPayloadError:
                        self.__not_loaded_files.append(file)

    async def download_content_from_thread(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__tread_url) as resp_with_json:
                if resp_with_json.status == 200:
                    posts = (await resp_with_json.json())['threads'][0]['posts']

            tasks = [asyncio.create_task(self.__download(session, file)) for post in posts for file in post.get('files', [])]
            await asyncio.gather(*tasks)
            # I don't know what to do with ClientPayloadError so...
            while self.__not_loaded_files:
                tasks = [asyncio.create_task(self.__download(session, file)) for file in self.__not_loaded_files]
                self.__not_loaded_files = []
                await asyncio.gather(*tasks)
