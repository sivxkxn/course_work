from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.links import association_table
from connection.db import Base

class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    website = Column(String)
    Products = relationship("Product", secondary=association_table)

    def __repr__(self):
        return "<shop(name='%s', website='%s'" % \
               (self.name, self.website)

    def to_tuple(self):
        return self.name, self.website

    def __init__(self, name: str, website: str):
        self.name = name
        self.website = website