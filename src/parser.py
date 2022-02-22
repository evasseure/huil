from src.token import *
from src.ast import *
from rich import print


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self, token_type):
        raise Exception("Invalid syntax:", token_type, self.lexer.column, self.lexer.line)

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
        elif token.type == FLOAT:
            self.eat(FLOAT)
            return NumNode(token, float(token.value))
        elif token.type == STRING:
            self.eat(STRING)
            return StringNode(token, token.value)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == ID:
            id_token = self.current_token
            self.eat(ID)
            if self.current_token.type == LPAREN:
                self.eat(LPAREN)
                args = []
                while True:
                    args.append(self.factor())
                    if self.current_token.type == RPAREN:
                        self.eat(RPAREN)
                        break
                    else:
                        self.eat(COMMA)
                return FunctionCallNode(id_token, id_token.value, args)

            return VariableNode(id_token, id=id_token.value)

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

    def function(self):
        # DEF variable LPAREN (variable COMMA)* (variable)? RPAREN COLON EOL (statement)*

        fn_token = self.current_token
        self.eat(DEF)
        id_token = self.current_token
        self.eat(ID)
        self.eat(LPAREN)
        args = []
        while self.current_token.type == ID:
            args.append(self.current_token.value)
            self.eat(ID)
            if self.current_token.type == RPAREN:
                self.eat(RPAREN)
                break
            else:
                self.eat(COMMA)
        self.eat(COLON)
        self.eat(EOL)

        statements = []
        function_columns = self.current_token.column
        while self.current_token.column == function_columns:
            statements.append(self.statement())
            self.eat(EOL)

        node = FunctionNode(fn_token, id=id_token.value, arguments=args, statements=StatementListNode(None, statements))
        return node

    def statement(self):
        if self.current_token.type == LET:
            return self.assignment()
        if self.current_token.type == DEF:
            return self.function()
        else:
            return self.expr()

    def statement_list(self):
        nodes = []
        while self.current_token.type != EOF:
            if self.current_token.type == EOL:
                self.eat(EOL)
                continue
            nodes.append(self.statement())
            print(nodes)
        return StatementListNode(None, nodes)

    def program(self):
        node = self.statement_list()
        self.eat(EOF)
        return node

    def parse(self):
        return self.program()
