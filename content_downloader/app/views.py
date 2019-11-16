from aiohttp import web
from .serializers.request import content_2ch_request_validate_schema, content_2ch_thread_object_schema
from content_downloader.ext.for_2ch.downloader import Downloader

routes = web.RouteTableDef()


@routes.get('/health')
async def hello(request):
    return web.json_response({'health': 'ok'})


@routes.get('/content/download/2ch')
async def download_content_2ch(request):
    thread_url = content_2ch_request_validate_schema.load(request.query)
    tread_obj = content_2ch_thread_object_schema.dump(thread_url)
    dir_name = tread_obj['thread_name']

    content_path = request.app.cm.create_and_get_content_dir(dir_name=dir_name)

    downloader = Downloader(tread_url=tread_obj['thread_url_json'], path_to_downloaded_content=content_path)
    await downloader.download_content_from_thread()

    zip_path = request.app.cm.zipify_content(path_from=content_path, zip_name=dir_name)

    request.app.cm.delete_content_dir(dir_name)

    header = {'Content-Disposition': f'attachment; filename="{dir_name}"'}
    del downloader
    return web.FileResponse(path=zip_path, headers=header)
