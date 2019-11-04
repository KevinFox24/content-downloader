from content_downloader.for_2ch.downloader import Downloader
from content_downloader.config import config
import uvloop
import asyncio


async def main():
    app = Downloader(tread_url=config['2CH']['thread_url'])
    await app.download_content_from_thread()


if __name__ == '__main__':
    uvloop.install()
    asyncio.run(main())

