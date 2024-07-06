from fastapi import APIRouter

order_routers =APIRouter(
    prefix='/orders'
)

@order_routers.get('/')
async def get_orders():
    return {'message': 'Welcome to the orders endpoint!'}

@order_routers.get('/c')
async def create_order():
    return {'message': 'Order created successfully!'}