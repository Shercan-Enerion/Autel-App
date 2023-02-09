# -----------------------------------modules-----------------------------
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from security.auth import auth_routes
from routes.routes import routes
from routes.main import main
from dotenv import load_dotenv
from os import getenv
load_dotenv()
# -----------------------------------run---------------

app = FastAPI(title='Server Autel',
              description='Server with all data for SAVANT', version='0.0.1')
templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(main)
app.include_router(auth_routes, prefix='/api')
app.include_router(routes)


if __name__ == '__main__':
    if getenv('MODE') == 'TEST':
        uvicorn.run('app:app', log_level='info',
                    access_log=True, reload=True)
    else:
        uvicorn.run(app='app:app', host='0.0.0.0', port=80,
                    log_level='info', access_log=False)
