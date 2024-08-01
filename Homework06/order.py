from fastapi import APIRouter, HTTPException
from db import orders, users, products, database
from models import Order, OrderIn

router = APIRouter()


@router.post('/orders/', response_model=Order)
async def create_order(order: OrderIn):
    is_user = await database.fetch_one(users.select().where(users.c.id == order.user_id))
    if not is_user:
        raise HTTPException(status_code=404, detail=f'User id={order.user_id} not found')
    is_product = await database.fetch_one(products.select().where(products.c.id == order.product_id))
    if not is_product:
        raise HTTPException(status_code=404, detail=f'Product id={order.product_id} not found')
    query = orders.insert().values(user_id=order.user_id, product_id=order.product_id, date=order.date,
                                   status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), 'id': last_record_id}


@router.get('/orders/', response_model=list[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@router.get('/orders/{order_id}', response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    res = await database.fetch_one(query)
    if res:
        return res
    raise HTTPException(status_code=404, detail=f'Order id={order_id} not found')


@router.put('/orders/{order_id}', response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    is_user = await database.fetch_one(users.select().where(users.c.id == new_order.user_id))
    if not is_user:
        raise HTTPException(status_code=404, detail=f'User id={new_order.user_id} not found')
    is_product = await database.fetch_one(products.select().where(products.c.id == new_order.product_id))
    if not is_product:
        raise HTTPException(status_code=404, detail=f'Product id={new_order.product_id} not found')
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    if await database.execute(query):
        return {**new_order.dict(), 'id': order_id}
    raise HTTPException(status_code=404, detail=f'Order id={order_id} not found')


@router.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    if await database.execute(query):
        return {'message': f'Order id={order_id} deleted'}
    raise HTTPException(status_code=404, detail=f'Order id={order_id} not found')
