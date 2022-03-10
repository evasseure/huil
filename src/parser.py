from src.token import *
from src.ast import *
from rich import print


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, token_type, error_message=None):
        if not error_message:
            raise Exception(f"Invalid syntax: {token_type} at (l{self.lexer.line + 1}:c{self.lexer.column + 1})")
        raise Exception(f"{error_message} at (l{self.lexer.line + 1}:c{self.lexer.column + 1})")

    def eat(self, token_type, error_message=None):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(self.current_token.type, error_message)

    def atom(self):
        token: Token = self.current_token
        if token.type == INTEGER:
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
            node = self.expression()
            self.eat(RPAREN)
            return node
        elif token.type == ID:
            id_token = self.current_token
            self.eat(ID)
            return VariableNode(id_token, id=id_token.value)

        # self.error(token.type)

    def primary(self):
        id_token: Token = self.current_token
        node = self.atom()
        token: Token = self.current_token
        if token.type == LPAREN:
            self.eat(LPAREN)
            args = []
            if self.current_token.type != RPAREN:
                while True:
                    args.append(self.expression())
                    if self.current_token.type == RPAREN:
                        self.eat(RPAREN)
                        break
                    else:
                        self.eat(COMMA)
            else:
                self.eat(RPAREN)
            return FunctionCallNode(id_token, id_token.value, args)
        return node

    def factor(self):
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            return UnaryOpNode(token, self.factor())
        elif token.type == MINUS:
            self.eat(MINUS)
            return UnaryOpNode(token, self.factor())
        elif token.type == NOT:
            self.eat(NOT)
            return UnaryOpNode(token, self.factor())
        return self.primary()

    def term(self):
        node = self.factor()
        while self.current_token.type in (MUL, DIV, INTDIV, MOD):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            elif token.type == INTDIV:
                self.eat(INTDIV)
            elif token.type == MOD:
                self.eat(MOD)

            node = BinaryOpNode(left=node, token=token, right=self.factor())

        return node

    def expression(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS, AND, OR, SUPEQUAL, INFEQUAL, SUP, INF, EQUAL, NOTEQUAL):
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
            elif token.type == NOTEQUAL:
                self.eat(NOTEQUAL)
            elif token.type == AND:
                self.eat(AND)
            elif token.type == OR:
                self.eat(OR)
            node = BinaryOpNode(left=node, token=token, right=self.term())

        return node

    def assignment(self):
        id_token = self.current_token

        # A single token lookahead recursive descent parser can’t see far enough to tell that it’s parsing an
        # assignment until after it has gone through the left-hand side and stumbled onto the =.
        # FRANCHEMENT, je saurais pas l'expliquer pour l'instant, je sais même pas si c'est correct
        expr = self.expression()
        if self.current_token.type == ASSIGN:
            self.eat(ASSIGN)
            return AssignmentNode(token=id_token, id=id_token.value, value=self.expression())

        return expr

    def declaration(self):
        self.eat(LET)
        assign_token = self.current_token
        id_token = self.current_token
        self.eat(ID, "Expected variable name, not: " + self.current_token.type)
        if self.current_token.type == ASSIGN:
            self.eat(ASSIGN)
            return DeclarationNode(token=assign_token, id=id_token.value, value=self.expression())
        else:
            return DeclarationNode(token=assign_token, id=id_token.value, value=NilNode(None))

    def function_def(self):
        fn_token = self.current_token
        self.eat(FN)
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
        self.eat(NEWLINE)
        return FunctionNode(fn_token, id=id_token.value, arguments=args, statements=self.statements(block=True))

    def if_stmt(self):
        token = self.current_token
        self.eat(IF)
        conditions = [self.expression()]
        self.eat(COLON)
        self.eat(NEWLINE)
        truthy_statements = [self.statements(block=True)]

        while self.current_token.type == ELIF:
            self.eat(ELIF)
            conditions.append(self.expression())
            self.eat(COLON)
            self.eat(NEWLINE)
            truthy_statements.append(self.statements(block=True))

        else_statements = []
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            self.eat(COLON)
            self.eat(NEWLINE)
            else_statements = self.statements(block=True)

        return IfThenElseNode(
            token,
            conditions,
            truthy_statements,
            else_statements,
        )

    def while_stmt(self):
        token = self.current_token
        self.eat(WHILE)
        condition = self.expression()
        self.eat(COLON)
        self.eat(NEWLINE)
        statements = self.statements(block=True)

        return WhileNode(
            token,
            condition,
            statements,
        )

    def return_stmt(self):
        token = self.current_token
        self.eat(RETURN)
        return ReturnNode(token, self.expression())

    def simple_stmt(self):
        if self.current_token.type == LET:
            return self.declaration()
        if self.current_token.type == ID:
            return self.assignment()
        if self.current_token.type == RETURN:
            return self.return_stmt()
        return self.expression()

    def compound_stmt(self):
        if self.current_token.type == IF:
            return self.if_stmt()
        if self.current_token.type == FN:
            return self.function_def()
        if self.current_token.type == WHILE:
            return self.while_stmt()

    def simple_stmts(self):
        stmt = self.simple_stmt()
        if stmt:
            self.eat(NEWLINE, "Expected newline")
        return stmt

    def statements(self, block=False):
        nodes = []

        current_indent = self.current_token.column
        while self.current_token.type != EOF and (not block or self.current_token.column == current_indent):
            # Skip empty lines
            if self.current_token.type == NEWLINE:
                self.eat(NEWLINE)
                continue

            cmp = self.compound_stmt()
            sim = self.simple_stmts()

            if cmp:
                nodes.append(cmp)

            if sim:
                nodes.append(sim)

        return StatementListNode(None, nodes)

    def parse(self):
        return self.statements()
