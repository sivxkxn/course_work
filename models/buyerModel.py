from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from connection.db import Base

class Buyer(Base):
    __tablename__ = 'buyer'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    phone = Column(Integer)

    Orders = relationship("Order", backref=backref("Order", uselist = False))
    #shops = relationship("Order", back_populates="buyers")

    def to_tuple(self):
        return self.name, self.address, self.phone

    def __repr__(self):
        return "<buyer(name='%s', address='%s' phone='%i')>" % \
               (self.name, self.address, self.phone)

    def __init__(self, name: str, address: str, phone: int):
        self.name = name
        self.address = address
        self.phone = phone
