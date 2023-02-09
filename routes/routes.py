# -----------------------------------modules-----------------------------
from security.verify_route import VerifyTokenRoute
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
from config.bd import dataBase
from requests import get
load_dotenv()

routes = APIRouter(route_class=VerifyTokenRoute)
# routes = APIRouter()

templates = Jinja2Templates(directory='templates')


@routes.get('/index', response_class=HTMLResponse)
async def mainindex(request: Request):
    data = dataBase.readDataData()[0]
    data.pop('_id')
    for k, _ in data.items():
        data[k]['All'] = 'All'
    clientes = dataBase.conn['Clients'].find()
    states = []
    cities = []
    clients = []
    for client in clientes:
        states.append(client['state'])
        cities.append(client['city'])
        clients.append(client['_id'])
    context = {'request': request, 'data': data,
               'states': states, 'cities': cities, 'clients': clients}
    response = templates.TemplateResponse('index.html', context=context)
    return response


@routes.get('/', response_class=HTMLResponse)
async def mainToIndex():
    response = RedirectResponse('/index')
    return response


@routes.get('/token', response_class=HTMLResponse)
async def mainTokenGet(request: Request):
    context = {'request': request}
    response = templates.TemplateResponse('token.html', context=context)
    return response
