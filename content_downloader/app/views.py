from aiohttp import web
from .serializers.request import content_2ch_request_schema
from content_downloader.ext.for_2ch.downloader import Downloader
from content_downloader.ext.zipper import zipify_content, clean_folder

routes = web.RouteTableDef()


@routes.get('/health')
async def hello(request):
    return web.json_response({'health': 'ok'})


@routes.get('/content/download')
async def hello(request):
    url = content_2ch_request_schema.load(request.query)['threadUrl']
    downloader = Downloader(tread_url=url)
    path = await downloader.download_content_from_thread()
    path_to_zip = zipify_content(path)
    clean_folder(path)
    return web.FileResponse(path=path_to_zip)
