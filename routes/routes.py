# -----------------------------------modules-----------------------------
from urllib.parse import unquote, quote_plus, quote
from security.verify_route import VerifyTokenRoute
from fastapi.templating import Jinja2Templates
from fastapi import Request, Form, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
from config.bd import dataBase
from requests import get
from requests import utils
import json
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


@routes.get('/companyrate', response_class=JSONResponse)
async def companiRates(value: str = '', sector: str = '', company: str = '', substr: str = ''):
    try:
        listCo = []
        if value == 'rates':
            response = get("https://api.openei.org/utility_rates?version=latest&format=json&api_key=XVKe43UvrJ0mduASGIthdBV2yCvzfdAjmaaW6cuZ&orderby=enddate&limit=30",
                           params={'sector': sector, 'ratesforutility': company})
            rangoCo = response.json()['items']
            for i in rangoCo:
                if i.get('enddate') == None:
                    listCo.append(i['name'])
        elif value == 'companies':
            response = get("https://openei.org/w/api.php?action=sfautocomplete&limit=500&format=json&category=EIA%20Utility%20Companies%20and%20Aliases" +
                           "&substr=" + substr)
            rangoCo = json.loads(response.content.decode())['sfautocomplete']
            for i in rangoCo:
                listCo.append(i['title'])
    except:
        listCo = {'data': 'error'}
    return listCo

# https: // api.openei.org/utility_rates?version = latest & detail = full & api_key = XVKe43UvrJ0mduASGIthdBV2yCvzfdAjmaaW6cuZ & format = json_plain & sector = Residential & orderby = enddate & limit = 30 & sector = Residential & ratesforutility = San % 20Diego % 20Gas % 20 % 26 % 20Electric % 20Co


@routes.get('/rates', response_class=JSONResponse)
async def companiRates(sector: str = '', company: str = '', rate: str = ''):
    response = get(
        f'https://api.openei.org/utility_rates?version=latest&detail=full&api_key=XVKe43UvrJ0mduASGIthdBV2yCvzfdAjmaaW6cuZ&format=json&orderby=enddate&limit=30&ratesforutility={company.replace("&","%26")}&sector={sector}')

    rangoCo = response.json()['items']
    for i in rangoCo:
        if i['name'] == rate:
            return i
    return {}
