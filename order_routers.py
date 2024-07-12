from fastapi import APIRouter, Depends, status 
from fastapi.encoders import jsonable_encoder 
from fastapi.exceptions import HTTPException 
from database import engine, SesionLocal 
from models import Order, User
from schemas import Order 
from fastapi_jwt_auth import AuthJWT
session = SesionLocal(bind=engine)

order_router = APIRouter( prefix="/order"
)

@order_router.get("/")
async def welcome_order(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise
    HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized")
    return {"message": "Hello order page!"}


@order_router.post("/create", response_model=Order) 
async def create_order(order: Order, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise
    HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    current_user = Authorize.get_jwt_subject() 
    user = session.query(User).filter(User.username == current_user).first()
    if not user:
        raise
    HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")

    new_order = Order(
        quanty=order.quanty,
        product_id=order.product_id,
        status="PENDING" 
    )
    new_order.user_id = user.id
    session.add(new_order)
    session.commit()
    session.refresh(new_order) # Refresh to get the new ID
    response_data = {    
        'id': new_order.id,
        'quanty': new_order.quanty,
        'user_id': new_order.user_id,
        'product_id': new_order.product_id,
        'order_status': new_order.status, # Ensure this is a string
    }
    return jsonable_encoder(response_data)


@order_router.get('/list')
async def get_orders(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required() 
    except Exception as e:
        raise
    HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unauthorized")
    user_id = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == user_id).first() 
    if not user:
        raise
    HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if user.is_staff:
        orders = session.query(Order).all()
    else:
        orders = session.query(Order).filter(Order.user_id == user.id).all()
        return orders
@order_router.get('/{id}')
async def get_order(id: int, Authorize: AuthJWT = Depends()): 
    try:
        Authorize.jwt_required() 
    except Exception as e:
        raise
    HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    order = session.query(Order).filter(Order.id == id).first() 
    if not user.id == order.user_id:
        raise
    HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden")
    if not order:
        raise
    HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    return order

@order_router.put('/{id}/update', response_model=Order)
async def update_order(id: int, order: Order, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required() 
    except Exception as e:
        raise
    HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    order = session.query(Order).filter(Order.id == id).first() 
    if not user.id == order.user_id:
        raise
    HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden")
    if not order:
        raise
    HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    order.quanty = order.quanty
    session.commit()
    session.refresh(order)
    return order

@order_router.delete('/{id}/delete', response_model=Order)
async def delete_order(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required() 
    except Exception as e:
        raise
    HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    order = session.query(Order).filter(Order.id == id).first() 
    if not user.id == order.user_id:
        raise
    HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden")
    if not order:
        raise
    HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    session.delete(order)
    session.commit()
    return order

@order_router.get('/{id}/status')
async def get_order_status(id: int, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required() 
    except Exception as e:
        raise
    HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    order = session.query(Order).filter(Order.id == id).first() 
    if not user.id == order.user_id:
        raise
    HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden")
    if not order:
        raise
    HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    return {"order_status": order.status}

@order_router.put('/{id}/status/{status}')
async def update_order_status(id: int, status: str, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required() 
    except Exception as e:
        raise
    HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized")
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    order = session.query(Order).filter(Order.id == id).first() 
    if not user.id == order.user_id:
        raise
    HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Forbidden")
    if not order:
        raise
    HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Order not found")
    order.status = status
    session.commit()
    session.refresh(order)
    return {"order_status": order.status}