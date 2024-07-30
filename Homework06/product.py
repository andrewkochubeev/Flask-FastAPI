from fastapi import APIRouter, HTTPException
from db import products, database
from models import Product, ProductIn
from random import randint

router = APIRouter()


@router.post('/fill_products/{count}')
async def fill_products(count: int):
    for i in range(count):
        query = products.insert().values(name=f'product{i + 1}', description=f'description{i + 1}',
                                         price=randint(1, 50) / randint(1, 5))
        await database.execute(query)
    return {'message': f'{count} fake products create'}


@router.post('/products/', response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(name=product.name, description=product.description, price=product.price)
    last_record_id = await database.execute(query)
    return {**product.dict(), 'id': last_record_id}


@router.get('/products/', response_model=list[Product])
async def read_products():
    query = products.select()
    return await database.fetch_all(query)


@router.get('/products/{product_id}', response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    res = await database.fetch_one(query)
    if res:
        return res
    raise HTTPException(status_code=404, detail=f'Product id={product_id} not found')


@router.put('/products/{product_id}', response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(**new_product.dict())
    if await database.execute(query):
        return {**new_product.dict(), 'id': product_id}
    raise HTTPException(status_code=404, detail=f'Product id={product_id} not found')


@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    if await database.execute(query):
        return {'message': f'Product id={product_id} deleted'}
    raise HTTPException(status_code=404, detail=f'Product id={product_id} not found')
