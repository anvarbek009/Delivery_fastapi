from fastapi import FastAPI
from auth_routers import auth_routers
from products import product_routers
from order_routers import order_routers
from fastapi_jwt_auth import AuthJWT
from schemas import Settings, LoginModel

app =FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth_routers)
app.include_router(product_routers)
app.include_router(order_routers)

@app.get('/')
async def get_home():
    return {'message': 'Welcome to the FastAPI-Auth API!'}

