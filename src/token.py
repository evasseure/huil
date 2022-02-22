from src.tokens import *


class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __str__(self):
        """String representation of the class instance."""
        return "Token({type}, {value})".format(type=self.type, value=repr(self.value))

    def __repr__(self):
        return self.__str__()
