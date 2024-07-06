from fastapi import FastAPI
from auth_routers import auth_routers
from products import product_routers
from order_routers import order_routers

app =FastAPI()

app.include_router(auth_routers)
app.include_router(product_routers)
app.include_router(order_routers)

app.get('/')
async def get_home():
    return {'message': 'Welcome to the FastAPI-Auth API!'}

