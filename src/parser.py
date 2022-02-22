from src.token import *
from src.ast import *
from rich import print


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self, token_type):
        raise Exception("Invalid syntax:", token_type)

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(self.current_token.type)

    def factor(self):
        """factor : (PLUS | MINUS factor) | INTEGER | LPAREN expr RPAREN"""
        token: Token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            return UnaryOpNode(token, self.factor())
        elif token.type == MINUS:
            self.eat(MINUS)
            return UnaryOpNode(token, self.factor())
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return NumNode(token, int(token.value))
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == ID:
            self.eat(ID)
            return VariableNode(token, id=token.value)

    def term(self):
        """term : factor ((MUL | DIV | MOD) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV, MOD):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == MOD:
                self.eat(MOD)

            node = BinaryOpNode(left=node, token=token, right=self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinaryOpNode(left=node, token=token, right=self.term())

        return node

    def assignment(self):
        # assignment: LET variable ASSIGN expr
        if self.current_token.type == LET:
            assign_token = self.current_token
            self.eat(LET)
            id_token = self.current_token
            self.eat(ID)
            self.eat(ASSIGN)
            node = AssignmentNode(token=assign_token, id=id_token, value=self.expr())

        return node

    def statement(self):
        if self.current_token.type == LET:
            return self.assignment()
        else:
            return self.expr()

    def statement_list(self):
        nodes = []
        while self.current_token.type != EOF:
            if self.current_token.type == EOL:
                self.eat(EOL)
                continue
            nodes.append(self.statement())
        return StatementListNode(None, nodes)

    def program(self):
        return self.statement_list()

    def parse(self):
        return self.program()
