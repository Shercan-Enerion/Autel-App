from fastapi import APIRouter, Header
from pydantic import BaseModel, EmailStr
from .jwt_functions import validate_token, write_token
from fastapi.responses import JSONResponse
from fastapi import Request, Form
from fastapi import FastAPI, Response
from starlette.status import HTTP_302_FOUND
from starlette.responses import RedirectResponse
from classobject.classes import signupClass, Hash
from config.bd import dataBase
from fastapi.templating import Jinja2Templates
from config.bd import dataBase
auth_routes = APIRouter()
templates = Jinja2Templates(directory='templates')


class User(BaseModel):
    email: EmailStr
    password: str


@auth_routes.post("/verify_token")
def verify_token(Authorization: str = Header(None)):
    token = Authorization.split(" ")[1]
    return validate_token(token, output=True)


@auth_routes.get('/registers', response_class=JSONResponse)
async def signup(request: Request):
    dataBase.readDataData
    context = {'request': request}
    response = JSONResponse(content=context)
    return response
