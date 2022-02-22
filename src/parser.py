from src.token import *
from src.ast import *
from rich import print


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self, token_type):
        raise Exception(f"Invalid syntax: {token_type} at (l{self.lexer.line}:c{self.lexer.column})")

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(self.current_token.type)

    def match(self):
        token = self.current_token
        self.eat(MATCH)
        compared = self.factor()
        self.eat(COLON)
        self.eat(EOL)

        matches = []
        match_columns = self.current_token.column
        while self.current_token.column == match_columns:
            self.eat(PIPE)
            if self.current_token.type == MUL:
                match = StringNode(self.current_token, "*")
                self.eat(MUL)
            else:
                match = self.factor()
            self.eat(ARROW)
            expr = self.expr()
            self.eat(EOL)
            matches.append([match, expr])

        return MatchNode(token, compared, matches)

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
        elif token.type == BOOLEAN:
            self.eat(BOOLEAN)
            return BooleanNode(token, token.value)
        elif token.type == STRING:
            self.eat(STRING)
            return StringNode(token, token.value)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == "MATCH":
            return self.match()
        elif token.type == ID:
            id_token = self.current_token
            self.eat(ID)
            if self.current_token.type == LPAREN:
                self.eat(LPAREN)
                args = []
                while True:
                    args.append(self.expr())
                    if self.current_token.type == RPAREN:
                        self.eat(RPAREN)
                        break
                    else:
                        self.eat(COMMA)
                return FunctionCallNode(id_token, id_token.value, args)
            elif self.current_token.type == ASSIGN:
                self.eat(ASSIGN)
                node = AssignmentNode(token=id_token, id=id_token.value, value=self.expr())
            else:
                return VariableNode(id_token, id=id_token.value)

    def term(self):
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

        while self.current_token.type in (PLUS, MINUS, SUPEQUAL, INFEQUAL, SUP, INF, EQUAL):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            elif token.type == SUPEQUAL:
                self.eat(SUPEQUAL)
            elif token.type == INFEQUAL:
                self.eat(INFEQUAL)
            elif token.type == SUP:
                self.eat(SUP)
            elif token.type == INF:
                self.eat(INF)
            elif token.type == EQUAL:
                self.eat(EQUAL)
            node = BinaryOpNode(left=node, token=token, right=self.term())

        return node

    def declaration(self):
        if self.current_token.type == LET:
            assign_token = self.current_token
            self.eat(LET)
            id_token = self.current_token
            self.eat(ID)
            if self.current_token.type == ASSIGN:
                self.eat(ASSIGN)
                return DeclarationNode(token=assign_token, id=id_token.value, value=self.expr())
            else:
                return DeclarationNode(token=assign_token, id=id_token.value, value=NilNode(None))

    def function(self):
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
            return self.declaration()
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
