# -----------------------------------modules-----------------------------
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
from starlette.responses import RedirectResponse
from fastapi import Request
from fastapi.websockets import WebSocket
from security.jwt_functions import write_token
from classobject.classes import signupClass, Hash
from config.bd import dataBase
from starlette.status import HTTP_302_FOUND
from security.jwt_functions import write_token
from typing import List

main = APIRouter()

templates = Jinja2Templates(directory='templates')


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        await websocket.close()

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()
datasNotFiltered = {}


@main.get('/signin', response_class=HTMLResponse)
async def signin(request: Request):
    context = {'request': request}
    response = templates.TemplateResponse('signin.html', context=context)
    return response


@main.post("/signin")
async def login(email: str = Form(), password: str = Form(), request: Request = None):
    try:
        user = list(dataBase.readUser(id=email))
    except:
        # sin conexión base de datos
        context = {'request': request, 'message': 'BD'}
        response = templates.TemplateResponse(
            'signin.html', context=context)
        return response
    if len(user) > 0:
        if Hash.verify_password(password, user[0]['password']):
            token = write_token({'email': email})
            response = RedirectResponse('/', status_code=HTTP_302_FOUND)
            response.set_cookie(key="Authorization", value=token)
        else:
            context = {'request': request, 'message': 'IP'}
            response = templates.TemplateResponse(
                'signin.html', context=context)
    else:
        context = {'request': request, 'message': 'ENT'}
        response = templates.TemplateResponse(
            'signin.html', context=context)
    return response


@main.post('/userin', response_class=HTMLResponse)
async def signin(username: str = Form(), password: str = Form(), email: str = Form(), code: str = Form(), request: Request = None):
    insert = None
    if code == 'autel':
        insert = signupClass.postUser(email=email, password=Hash.get_password_hash(
            password), username=username)

    if insert is not None:
        context = {'request': request, 'message': 'User created'}
        response = templates.TemplateResponse('signin.html', context=context)
        return response
    else:
        context = {'request': request, 'message': 'AAC'}
        response = templates.TemplateResponse('signup.html', context=context)
        return response


@main.get('/signup', response_class=HTMLResponse)
async def signup(request: Request):
    context = {'request': request}
    response = templates.TemplateResponse('signup.html', context=context)
    return response
