from fastapi  import APIRouter

auth_routers=APIRouter(
    prefix="/auth"
)

@auth_routers.get('/')
async def get_auth():
    return {'message': 'Welcome to the authentication endpoint!'}