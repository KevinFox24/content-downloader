from aiohttp import web
from .views import routes
from .middlewares import validation_error_middleware


app = web.Application(middlewares=[validation_error_middleware])
app.add_routes(routes)
