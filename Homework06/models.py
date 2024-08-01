from pydantic import BaseModel, Field, EmailStr
from datetime import date
from werkzeug.security import generate_password_hash


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    surname: str = Field(max_length=64)
    email: EmailStr = Field(max_length=128)
    password: str = Field(max_length=128)



class User(UserIn):
    id: int


class ProductIn(BaseModel):
    name: str = Field(max_length=32)
    description: str = Field(max_length=128)
    price: float = Field(gt=0)


class Product(ProductIn):
    id: int


class OrderIn(BaseModel):
    user_id: int
    product_id: int
    date: date
    status: bool = Field(default=False)


class Order(OrderIn):
    id: int
