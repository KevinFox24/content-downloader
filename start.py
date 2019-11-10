from content_downloader.app.app import app
from aiohttp import web
import uvloop


if __name__ == '__main__':
    uvloop.install()
    web.run_app(app)
