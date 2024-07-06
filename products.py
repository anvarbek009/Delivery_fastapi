from fastapi import APIRouter

product_routers=APIRouter(
    prefix='/products'
)

@product_routers.get('/')
async def get_products():
    return {'message': 'Welcome to the products endpoint!'}