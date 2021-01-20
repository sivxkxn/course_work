from texttable import Texttable
from termcolor import colored
import matplotlib.pyplot as plt
from models.ExceptionsModel import *

class View:

    def DisplayMenu(self):
        print(
            "Choose table : \n1.Show shops \n2.Show orders per month"
            + "\n3.Generate data"
            + "\n4.Show amount of orders for every month\n5.Insert"
            + "\n6.Show graphics for year\n7.Show orders for a certain date" +
            "\n0.Exit"
        )

    def PrintInform(self, message):
        print(message)

    def ShowTable(self, table_name, columns, rows):
        print(
            "______________________________________________________________"
            + f"\n{table_name}"
        )
        table = Texttable()
        if type(rows) == tuple:
            rows = [rows]
        rows = [columns] + rows
        table.add_rows(rows)
        table.header(columns)
        print(table.draw())
        print(
            "______________________________________________________________"
        )

    def ShowGraph(self, arrays, names, xlabel, ylabel, title, filename):
        print("khj")

    def ShowGraphMonth(self, x,y, xlabel, ylabel, title, filename):
        fig, ax = plt.subplots()
        x_data = x
        y_data = y
        print(x_data)
        print(y_data)

        ax.bar(x_data, y_data, color='#C88BDD')
        ax.set(xlabel=xlabel, ylabel=ylabel, title=title)
        fig.set_figwidth(12)
        fig.set_figheight(6)
        if filename:
            fig.savefig(filename)
        plt.show()

    def InsertEntity(self, entity_name, columns, rows):
        self.ShowTable(f"{entity_name} was added\n", columns, rows)

    def NoSuchCommandError(self):
        print(colored("No such command", "red"))

    def InputException(self, e):
        if type(e) == NegativeInputException:
            NegativeInputException(e.name)
        errors = {NegativeInputException: self.NegativeInputError,
                  DateInputException: self.DateInputException,
                  EmptyInputException: self.EmptyInputError,
                  ValueException: self.ValueError}
        errors[type(e)](e.name)

    def NegativeInputError(self, name):
        print(colored(f"Incorrect input, {name} should be positive", "red"))

    def DateInputException(self, name):
        print(colored(f"Incorrect input, {name} is incorrect date", "red"))

    def EmptyInputError(self, name):
        print(colored(f"Incorrect input, {name} shouldn't be empty", "red"))

    def ValueError(self, name):
        print(colored(f"Incorrect input, {name} invalid value", "red"))

    def EntityAlreadyExistsException(self, e):
        print(colored(f"This {e.name} already exists", "red"))

    def EntityDoesntExistException(self, e):
        print(colored(f"This {e.name} doesn't exist", "red"))

    def RecordsNotFound(self, e):
        print(colored(f"{e.name} records not found", "red"))

    def UnknownException(self, e):
        print(colored(f"Error: {e}", "red"))

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def InputPositiveInt(self, name):
        value = input(f"Enter {name}: ")
        if value == "":
            raise EmptyInputException(name)
        try:
            value = int(value)
            if value < 0:
                raise NegativeInputException(name)
        except ValueError:
            raise ValueException(name)
        return value

    def InputPositiveFloat(self, name):
        value = input(f"Enter {name}: ")
        if value == "":
            raise EmptyInputException(name)
        try:
            value = float(value)
            if value < 0:
                raise NegativeInputException(name)
        except ValueError:
            raise ValueException(name)
        return value

    def InputYearMonth(self):
        year = self.InputPositiveInt("year ")
        if year > 2020 or year < 1990:
            raise DateInputException(year)
        res = str(year)
        month = self.InputPositiveInt("month number ")
        if month < 0 or month > 12:
            raise DateInputException(month)
        if month < 10:
            month = "0" + str(month)
            res = res + '-' + month
        else:
            res = res + '-' + str(month)
        return res

    def InputYear(self):
        year = self.InputPositiveInt("year ")
        if year > 2020 or year < 2015:
            raise DateInputException(year)
        res = str(year)
        return res

    def InputDate(self):
        year = self.InputPositiveInt("year")
        if year > 2020 or year < 1990:
            raise DateInputException(year)
        res = str(year)
        month = self.InputPositiveInt("month")
        if month > 12:
            raise DateInputException(month)
        if month < 10:
            month = "0" + str(month)
            res = res + '-' + month
        else:
            res = res + '-' + str(month)
        day = self.InputPositiveInt("day")
        if day > 31:
            raise DateInputException(day)
        if day < 10:
            day = "0" + str(day)
            res = res + '-' + day
        else:
            res = res + '-' + str(day)
        return res

    def InputCommand(self):
        return self.InputPositiveInt("command")

    def InputString(self, name):
        value = input(f"Enter {name} : ")
        value = value.strip()
        if value == "":
            raise EmptyInputException(name)
        return value

    def InputBool(self, question):
        ch = input(question + " [y/n]: ")
        return ch == 'y' or ch == 'Y'
