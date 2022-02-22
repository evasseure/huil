from tokenize import Token
from src.reserved_keywords import RESERVED_KEYWORDS

from src.token import *


class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self, char):
        raise Exception("Invalid character:", char)

    def advance(self, amount=1):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += amount
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self, char_number=1) -> str or None:
        if self.pos + char_number > len(self.text) - 1:
            return None
        else:
            return self.text[self.pos : self.pos + char_number]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != "\n":
            self.advance()
        self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from the input."""
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return int(result)

    def id(self):
        result = ""
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        return RESERVED_KEYWORDS.get(result, Token(ID, result))

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:
            self.current_char: str  # Specifying the type

            if self.current_char.isspace():
                if self.current_char == "\n":
                    self.advance()
                    return Token(EOL, None)
                else:
                    self.skip_whitespace()
                continue

            if self.current_char == "/" and self.peek() == "/":
                self.skip_comment()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char.isalpha():
                if self.peek(3) == "let":
                    self.advance(3)
                    return Token(LET, "let")
                else:
                    return self.id()

            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")

            if self.current_char == "*":
                self.advance()
                return Token(MUL, "*")

            if self.current_char == "%":
                self.advance()
                return Token(MOD, "%")

            if self.current_char == "/":
                self.advance()
                return Token(DIV, "/")

            if self.current_char == "(":
                self.advance()
                return Token(LPAREN, "(")

            if self.current_char == ")":
                self.advance()
                return Token(RPAREN, ")")

            if self.current_char == "=":
                self.advance()
                return Token(ASSIGN, "=")

            self.error(self.current_char)

        return Token(EOF, None)
