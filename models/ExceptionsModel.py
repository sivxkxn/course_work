class InputException(Exception):
    pass
class  DateInputException(InputException):
    def __init__(self, name):
        self.name = name

class NegativeInputException(InputException):
    def __init__(self, name):
        self.name = name

class EmptyInputException(InputException):
    def __init__(self, name):
        self.name = name

class ValueException(InputException):
    def __init__(self, name):
        self.name = name

class EntityAlreadyExistsException(Exception):
    def __init__(self, name):
        self.name = name

class EntityDoesntExistException(Exception):
    def __init__(self, name):
        self.name = name


class RecordsNotFound(Exception):
    def __init__(self, name):
        self.name = name