from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.links import association_table
from connection.db import Base


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    Shops = relationship("Shop", secondary=association_table)

    def __repr__(self):
        return "<product(name='%s', price='%i')>" % \
               (self.name, self.price)

    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price
        # self.id_shop = id_shop
        # self.id_order = id_order

    def to_tuple(self):
        return self.name, self.price
