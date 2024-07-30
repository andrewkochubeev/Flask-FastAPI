import sqlalchemy
import databases
from settings import settings

DATABASE_URL = settings.DATABASE_URL
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    'users', metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(32)),
    sqlalchemy.Column('surname', sqlalchemy.String(64)),
    sqlalchemy.Column('email', sqlalchemy.String(128)),
    sqlalchemy.Column('password', sqlalchemy.String(128))
)

products = sqlalchemy.Table(
    'products', metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('name', sqlalchemy.String(32)),
    sqlalchemy.Column('description', sqlalchemy.String(128)),
    sqlalchemy.Column('price', sqlalchemy.Float())
)

orders = sqlalchemy.Table(
    'orders', metadata,
    sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('user_id', sqlalchemy.ForeignKey(users.c.id)),
    sqlalchemy.Column('product_id', sqlalchemy.ForeignKey(products.c.id)),
    sqlalchemy.Column('date', sqlalchemy.Date()),
    sqlalchemy.Column('status', sqlalchemy.Boolean())
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={'check_same_thread': False}
)

metadata.create_all(engine)
