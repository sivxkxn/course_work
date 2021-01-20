import time
from sqlalchemy import text, func
from models.productModel import Product
from models.orderModel import Order
from models.shopModel import Shop
from models.buyerModel import Buyer
from connection.db import session

from models.ExceptionsModel import EntityAlreadyExistsException, EntityDoesntExistException, RecordsNotFound


class Model:
    def AllShops(self):
        try:
            shops = session.query(Shop).order_by(Shop.id).all()
            return ['name', 'website'], [entity.to_tuple() for entity in shops]
        except Exception as err:
            print("Get error in get all Shops: ", err)
            exit(1)

    def OrdersLastDays(self, start: str, end: str):
        try:
            orders = session.query(Order) \
                .filter(text(f" date > \'{start}\' and date < \'{end}\' ")).all()
            return ['fk_buyer', 'fk_product', 'date'], [entity.to_tuple() for entity in orders]
        except Exception as err:
            print("Get error in orders last days: ", err)
            exit(1)

    def OrdersByMonth(self, month: int):
        try:
            orders = session.query(Order) \
                .filter(text(f"date::text LIKE \'{month}%\'")) \
                .order_by(Order.id).all()
            return ['fk_buyer', 'fk_product', 'date'], [entity.to_tuple() for entity in orders]
        except Exception as err:
            print("Get error in get orders by month: ", err)
            exit(1)

    def AvgAmountMonthInYear(self, year: int):
        try:
            array = [[]]
            for i in range(1, 13):
                date = str(year)
                if i < 10:
                    date = date + '-0' + str(i)
                else:
                    date = date + '-' + str(i)
                orders = session.query(func.count(Order.id)) \
                    .filter(text(f"date::text LIKE \'{date}%\'")).one()
                value = str(orders)
                value = value[1:-2]

                array.append([str(i), value])
            array.pop(0)
            return ['month', 'count'], array
        except Exception as err:
            print("Get error in get all orders by year: ", err)
            exit(1)

    def MakeAvgGraphMonth(self, date):
        xdata = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
                 'november', 'december']
        array = []
        for i in range(1, 13):
            date_ = str(date)
            if i < 10:
                date_ = date_ + '-0' + str(i)
            else:
                date_ = date_ + '-' + str(i)
            orders = session.query(func.count(Order.id)).filter(text(f"date::text LIKE \'{date_}%\'")).one()
            #orders = session.query(Order).join(Product).filter(text(f"date::text LIKE \'{date_}%\'")).one()
            value = str(orders)

            value = value[1:-2]

            array.append(int(value))
        return xdata, array

    def FindShopBool(self, id: int):
        try:
            session.query(Shop) \
                .filter(Shop.id == id).one()
            return True
        except Exception:
            return False

    def FindBuyerBool(self, id: int):
        try:
            session.query(Buyer) \
                .filter(Buyer.id == id).one()
            return True
        except Exception:
            return False

    def FindProductBool(self, id: int):
        try:
            session.query(Product) \
                .filter(Product.id == id).one()
            return True
        except Exception:
            return False

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def InsertBuyer(self, buyer):
        try:
            if session.query(Buyer).filter(Buyer.name == buyer[0], Buyer.address == buyer[1], Buyer.phone == buyer[2]).all():
                raise EntityAlreadyExistsException("buyer")
            buy = Buyer(buyer[0], buyer[1], buyer[2])
            session.add(buy)
            session.commit()
            return ['name', 'address', 'phone'], [buy.to_tuple()]
        except Exception as err:
            print("Error - cannot add buyer", err)

    def InsertProduct(self, product):
        try:
            if session.query(Product).filter(Product.name == product[0]).all():
                raise EntityAlreadyExistsException("product")
            entity = Product(product[0], product[1])
            session.add(entity)
            session.commit()
            return ['name', 'price'], [entity.to_tuple()]
        except Exception as err:
            print("Add product error! ", err)

    def InsertOrder(self, ent):
        try:
            if session.query(Order).filter(Order.date == ent[0]).all():
                raise EntityAlreadyExistsException("order")
            entity = Order(ent[0], ent[1], ent[2])
            session.add(entity)
            session.commit()
            return ['fk_buyer', 'fk_product', 'date'], [entity.to_tuple()]
        except Exception as err:
            print("Add order error! ", err)

    def InsertShop(self, ent):
        try:
            if session.query(Shop).filter(Shop.name == ent[0]).all():
                raise EntityAlreadyExistsException("shop")
            entity = Shop(ent[0], ent[1])
            session.add(entity)
            session.commit()
            return ['name', 'website'], [entity.to_tuple()]
        except Exception as err:
            print("Add shop error! ", err)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def GenerateShopProducts(self, rows: int):
        try:
            startTime = time.time()
            print('\nRows generating...')
            rows = session.execute(f" SELECT distinct row_shop ({rows}), "
                                   f" row_product({rows}) "
                                   f"FROM generate_series(1, {rows})")
            for row in rows:
                session.execute(f"INSERT  INTO \"shop_product\" (fk_shop, fk_product)"
                                f" values {row}")
            session.commit()
            endTime = time.time()
            print('Rows generated! Elapsed time: ' + str(endTime - startTime)[:9] + 's')
        except Exception as err:
            print("Generate rows error! ", err)

    def GenerateBuyer(self, rows: int):
        try:
            startTime = time.time()
            print('\nRows generating...')
            session.execute(f"INSERT  INTO \"buyer\" (name, address, phone)"
                            f" SELECT random_string(20),"
                            f" random_string(25),"
                            f" trunc(random()*(10000000))"
                            f" FROM generate_series(1, {rows})")
            session.commit()
            endTime = time.time()
            print('Rows generated! Elapsed time: ' + str(endTime - startTime)[:9] + 's')
        except Exception as err:
            print("Generate rows error! ", err)

    def GenerateProduct(self, rows: int):
        try:
            startTime = time.time()
            print('\nRows generating...')
            session.execute(f"INSERT  INTO \"product\" (name,price)"
                            f" SELECT random_string(25),"
                            f" trunc(random()*(1000))"
                            f" FROM generate_series(1, {rows})")
            session.commit()
            endTime = time.time()
            print('Rows generated! Elapsed time: ' + str(endTime - startTime)[:9] + 's')
        except Exception as err:
            print("Generate rows error! ", err)

    def GenerateOrder(self, rows: int):
                try:
                    startTime = time.time()
                    print('\nRows generating...')
                    session.execute(f"INSERT  INTO \"order\" (fk_buyer,fk_product,date)"
                                    f" SELECT row_buyer({rows}),"
                                    f" row_product({rows}),"
                                    f" ('2015/01/01'::date + trunc(random() * ('2021/01/14'::date - '2015/01/01'::date))* '1 day'::interval)"
                                    f" FROM generate_series(1, {rows})")
                    session.commit()
                    endTime = time.time()
                    print('Rows generated! Elapsed time: ' + str(endTime - startTime)[:9] + 's')
                except Exception as err:
                    print("Generate rows error! ", err)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
