import asyncio
from datetime import datetime
from sanic import Sanic
import sanic
from sanic.log import logger as log
from sanic.response import HTTPResponse, json
import uuid
import time

app = Sanic("Public Game Auth API")
app.config.FALLBACK_ERROR_FORMAT = "json"
app.config.DEBUG = True

token_cache = {}
TIMEOUT_SECONDS = 120

@app.post("/register")
async def register(request: sanic.Request) -> HTTPResponse:
    required = ['username', 'password', 'email', 'deviceID']
    if not all(item in request.json.keys() for item in required):
        return json({'code': 400, 'success': False, 'message': "Invalid request"}, 400)

    # TODO: save information in database

# Client sends user/pass and gets token to send to game server (Only valid for a few minutes, one time use)
@app.post("/authorize")
async def authenticate(request: sanic.Request) -> HTTPResponse:
    required = ['username', 'password']
    if not all(item in request.json.keys() for item in required):
        return json({'code': 400, 'success': False, 'message': "Invalid request"}, 400)

    # TODO: search authentication through database

    token = str(uuid.uuid4())
    token_cache[token] = {
        'username': request.json.get('username'),
        'nonce': time.time()
    }

    return json({
        'code': 200,
        'success': True,
        'data': {
            'token': token
        }
    }, 200)

# game server sends token to get user information
@app.post("/grant")
async def grant(request: sanic.Request) -> HTTPResponse:
    required = ['token']
    if not all(item in request.json.keys() for item in required):
        return json({'code': 400, 'success': False, 'message': "Invalid request"}, 400)

    data = token_cache.get(request.json.get('token'), None)
    if data is None:
        return json({'code': 404, 'success': False, 'message': "User is not authenticated"}, 404)

    del token_cache[request.json.get('token')]

    if time.time() - data.get('nonce') > TIMEOUT_SECONDS:
        return json({'code': 404, 'success': False, 'message': "User is not authenticated"}, 404)

    return json({
        'code': 200,
        'success': True,
        'data': data
    }, 200)


if __name__ == "__main__":
    app.run("0.0.0.0", 80, debug=False, access_log=False)