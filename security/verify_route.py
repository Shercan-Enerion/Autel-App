from fastapi import Request
from .jwt_functions import validate_token
from fastapi.routing import APIRoute
from starlette.responses import RedirectResponse


class VerifyTokenRoute(APIRoute):
    def get_route_handler(self):
        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            try:
                token = request.headers["cookie"].split("=")[1]
                validation_response = validate_token(token, output=True)
                if validation_response != None:
                    return await original_route(request)
                else:
                    return validation_response
            except:
                return RedirectResponse('/signin')
        return verify_token_middleware
