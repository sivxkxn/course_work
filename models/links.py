from sqlalchemy import Column, Integer, Table, ForeignKey
from connection.db import Base

association_table = Table(
    'shop_product', Base.metadata,
    Column('fk_shop', Integer, ForeignKey('shop.id')),
    Column('fk_product', Integer, ForeignKey('product.id'))
)
