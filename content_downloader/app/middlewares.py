from aiohttp import web
from marshmallow import ValidationError


@web.middleware
async def validation_error_middleware(request, handler):
    try:
        response = await handler(request)
    except ValidationError as e:
        return web.json_response({'ValidationError': e.normalized_messages()})
    else:
        return response
