from fastapi import APIRouter, HTTPException
from db import users, database
from models import User, UserIn

router = APIRouter()


@router.post('/fill_users/{count}')
async def fill_users(count: int):
    for i in range(count):
        query = users.insert().values(name=f'user{i + 1}', surname=f'surname{i + 1}', email=f'user{i + 1}@mail.ru',
                                      password=f'00{i + 1}')
        await database.execute(query)
    return {'message': f'{count} fake users create'}


@router.post('/users/', response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name, surname=user.surname, email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), 'id': last_record_id}


@router.get('/users/', response_model=list[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@router.get('/users/{user_id}', response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    res = await database.fetch_one(query)
    if res:
        return res
    raise HTTPException(status_code=404, detail=f'User id={user_id} not found')


@router.put('/users/{user_id}', response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    if await database.execute(query):
        return {**new_user.dict(), 'id': user_id}
    raise HTTPException(status_code=404, detail=f'User id={user_id} not found')


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    if await database.execute(query):
        return {'message': f'User id={user_id} deleted'}
    raise HTTPException(status_code=404, detail=f'User id={user_id} not found')
