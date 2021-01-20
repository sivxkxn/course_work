import model
import view

from models.ExceptionsModel import *


class Controller:
    def __init__(self):
        self.model = model.Model()
        self.view = view.View()

    def start(self):
        commands = [self.ShowAllShops, self.AllOrdersByMonth, self.Generate,
                    self.AvgAmountMonthInYear, self.Insert, self.ShowAvgGraph, self.OrdersLastDays]
        while True:
            try:
                self.view.DisplayMenu()
                ch = self.view.InputCommand()
            except Exception as e:
                self.HandleException(e)
                continue
            if ch == 0:
                break
            try:
                command = commands[ch - 1]
            except IndexError:
                self.view.NoSuchCommandError()
                continue
            try:
                command()
            except Exception as e:
                self.HandleException(e)

    def HandleException(self, e):
        if isinstance(e, InputException):
            self.view.InputException(e)
        elif isinstance(e, EntityAlreadyExistsException):
            self.view.EntityAlreadyExistsException(e)
        elif isinstance(e, EntityDoesntExistException):
            self.view.EntityDoesntExistException(e)
        elif isinstance(e, RecordsNotFound):
            self.view.RecordsNotFound(e)
        else:
            self.view.UnknownException(e)

    def ShowAllShops(self):
        columns, rows = self.model.AllShops()
        self.view.ShowTable("Shops", columns, rows)

    def AllOrdersByMonth(self):
        month = self.view.InputYearMonth()
        columns, rows = self.model.OrdersByMonth(month)
        self.view.ShowTable("Orders", columns, rows)

    def AvgAmountMonthInYear(self):
        year = self.view.InputPositiveInt("year")
        if year > 2020 or year < 2015:
            raise DateInputException(year)
        columns, rows = self.model.AvgAmountMonthInYear(year)
        self.view.ShowTable("Number of the orders per year", columns, rows)

    def OrdersLastDays(self):
        print("Enter start data")
        start = self.view.InputDate()
        print("Enter end data")
        end = self.view.InputDate()
        columns, rows = self.model.OrdersLastDays(start, end)
        self.view.ShowTable("Orders last 5 day", columns, rows)

    def ShowAvgGraph(self):
        date = self.view.InputYear()
        saveToFile = self.view.InputBool("Do you want to save graph to file?")
        filename = None
        if saveToFile:
            filename = f"graphics/{self.view.InputString('filename')}.png"

        x,y = self.model.MakeAvgGraphMonth(date)
        self.view.ShowGraphMonth(x,y,'Month', 'Value', 'Graph per year', filename)


    def Generate(self):
        print("Choose table:\n1.Buyer\n2.Shop_Product\n3.Product\n4.Order")
        command = self.view.InputCommand()
        if command < 1 or command > 5:
            self.view.NoSuchCommandError()
        rows = self.view.InputPositiveInt("rows")
        if command == 1:
            self.model.GenerateBuyer(rows)
            self.view.PrintInform("Random buyer successfully generated\n")
        elif command == 2:
            self.model.GenerateShopProducts(rows)
            self.view.PrintInform("Random shop_product successfully generated\n")
        elif command == 3:
            self.model.GenerateProduct(rows)
            self.view.PrintInform("Random product successfully generated\n")
        elif command == 4:
            self.model.GenerateOrder(rows)
            self.view.PrintInform("Random order successfully generated\n")

    def Insert(self):
        print("Choose table:\n1.Buyer\n2.Shop\n3.Product\n4.Order")
        command = self.view.InputCommand()
        if command < 1 or command > 5:
            self.view.NoSuchCommandError()
        if command == 1:
            name = self.view.InputString("name")
            address = self.view.InputString("address")
            phone = self.view.InputPositiveInt("phone")


            columns, rows = self.model.InsertBuyer([name, address, phone])
            self.view.InsertEntity("Buyer", columns, rows)
        elif command == 2:

            name = self.view.InputString("name")
            website = self.view.InputString("website")

            columns, rows = self.model.InsertShop([name, website])
            self.view.InsertEntity("Shop", columns, rows)
        elif command == 3:
            name = self.view.InputString("name")
            price = self.view.InputPositiveFloat("price")

            columns, rows = self.model.InsertProduct([name, price])
            self.view.InsertEntity("Product", columns, rows)
        elif command == 4:

            fk_buyer = self.view.InputPositiveInt("fk_buyer")
            fk_product = self.view.InputPositiveInt("fk_product")
            if self.model.FindBuyerBool(fk_buyer) == 0:
                raise RecordsNotFound("fk_buyer")
            if self.model.FindProductBool(fk_product) == 0:
                raise RecordsNotFound("fk_product")
            date = self.view.InputDate()

            columns, rows = self.model.InsertOrder([fk_buyer, fk_product, date])
            self.view.InsertEntity("Order", columns, rows)
