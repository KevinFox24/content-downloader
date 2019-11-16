from aiohttp import web
from .views import routes
from .middlewares import validation_error_middleware
from content_downloader.ext.content_manager import ContentManager
from content_downloader.config import download_path, create_zip_path


app = web.Application(middlewares=[validation_error_middleware])
app.add_routes(routes)

app.cm = ContentManager(download_path=download_path, zip_path=create_zip_path)
