from sqlalchemy import Column, Integer, String, Date, func, ForeignKey
from sqlalchemy.orm import relationship, backref
from connection.db import Base

class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    fk_buyer = Column(Integer, ForeignKey('buyer.id'))
    fk_product = Column(Integer, ForeignKey('product.id'))

    date = Column(Date, default=func.now())


    Products = relationship("Product", backref=backref("Product", uselist=False))
    Buyers = relationship("Buyer", backref=backref("Product", uselist=False))
    def to_tuple(self):
        return self.fk_buyer, self.fk_product, self.date

    def __repr__(self):
        return "<order(fk_buyer='%i', fk_product='%i', date='%s')>" % \
               (self.id_buyer, self.id_product, self.date)

    def __init__(self, fk_buyer: int, fk_product: int, date: str):
        self.fk_buyer = fk_buyer
        self.fk_product = fk_product
        self.date = date
