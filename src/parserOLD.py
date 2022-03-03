from src.token import *
from src.ast import *
from rich import print


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self, token_type):
        raise Exception(f"Invalid syntax: {token_type} at (l{self.lexer.line + 1}:c{self.lexer.column + 1})")

    def eat(self, token_type, error_message=None):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(self.current_token.type)

    # def match(self):
    #     token = self.current_token
    #     self.eat(MATCH)
    #     compared = self.factor()
    #     self.eat(COLON)
    #     self.eat(EOL)

    #     matches = []
    #     match_columns = self.current_token.column
    #     while self.current_token.column == match_columns:
    #         self.eat(PIPE)
    #         if self.current_token.type == MUL:
    #             match = StringNode(self.current_token, "*")
    #             self.eat(MUL)
    #         else:
    #             match = self.factor()
    #         self.eat(ARROW)
    #         expression = self.expression()
    #         self.eat(EOL)
    #         matches.append([match, expression])

    #     return MatchNode(token, compared, matches)

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
            return NumNode(token)
        elif token.type == FLOAT:
            self.eat(FLOAT)
            return NumNode(token)
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
            else:
                return VariableNode(id_token, id=id_token.value)

        self.error(token.type)

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

    def expression(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS, AND, OR, SUPEQUAL, INFEQUAL, SUP, INF, EQUAL):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            elif token.type == AND:
                self.eat(AND)
            elif token.type == OR:
                self.eat(OR)
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

    def assignment(self):
        id_token = self.current_token
        # self.eat(ID)
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

    # def function(self):
    #     fn_token = self.current_token
    #     self.eat(FN)
    #     id_token = self.current_token
    #     self.eat(ID)
    #     self.eat(LPAREN)
    #     args = []
    #     while self.current_token.type == ID:
    #         args.append(self.current_token.value)
    #         self.eat(ID)
    #         if self.current_token.type == RPAREN:
    #             self.eat(RPAREN)
    #             break
    #         else:
    #             self.eat(COMMA)
    #     self.eat(COLON)
    #     self.eat(EOL)

    #     statements = []
    #     function_columns = self.current_token.column
    #     while self.current_token.column == function_columns:
    #         statements.append(self.statement())
    #         self.eat(EOL)

    #     node = FunctionNode(fn_token, id=id_token.value, arguments=args, statements=StatementListNode(None, statements))
    #     return node

    # def if_control_flow(self):
    #     if_token = self.current_token
    #     self.eat(IF)
    #     conditions = [self.expression()]
    #     self.eat(COLON)
    #     self.eat(EOL)
    #     if_statements = []
    #     statements_columns = self.current_token.column
    #     while self.current_token.column == statements_columns:
    #         if_statements.append(self.statement())
    #         self.eat(EOL)
    #     truthy_statements = [if_statements]

    #     while self.current_token.type == ELIF:
    #         self.eat(ELIF)
    #         conditions.append(self.expression())
    #         self.eat(COLON)
    #         self.eat(EOL)
    #         elif_statements = []
    #         statements_columns = self.current_token.column
    #         while self.current_token.column == statements_columns:
    #             elif_statements.append(self.statement())
    #             self.eat(EOL)
    #         truthy_statements.append(elif_statements)

    #     else_statements = []
    #     if self.current_token.type == ELSE:
    #         self.eat(ELSE)
    #         self.eat(COLON)
    #         self.eat(EOL)
    #         statements_columns = self.current_token.column
    #         while self.current_token.column == statements_columns:
    #             else_statements.append(self.statement())
    #             self.eat(EOL)

    #     return IfThenElseNode(
    #         if_token,
    #         conditions,
    #         [StatementListNode(None, statm) for statm in truthy_statements],
    #         StatementListNode(None, else_statements),
    #     )

    # def statement(self):
    #     if self.current_token.type == LET:
    #         return self.declaration()
    #     if self.current_token.type == FN:
    #         return self.function()
    #     if self.current_token.type == IF:
    #         return self.if_control_flow()
    #     else:
    #         return self.expression()

    # def statement_list(self):
    #     nodes = []
    #     while self.current_token.type != EOF:
    #         if self.current_token.type == EOL:
    #             self.eat(EOL)
    #             continue
    #         nodes.append(self.statement())
    #     return StatementListNode(None, nodes)

    def simple_stmt(self):
        if self.current_token.type == LET:
            return self.declaration()
        if self.current_token.type == ID:
            return self.assignment()
        return self.expression()

    def compound_stmt(self):
        # | function_def
        # | if_stmt
        # | match_stmt
        # if self.current_token.type == IF:
        #     return self.if_control_flow()
        # if self.current_token.type == FN:
        #     return self.function()
        ...

    def simple_stmts(self):
        stmt = self.simple_stmt()
        self.eat(NEWLINE, "Expected newline")
        return stmt

    def statements(self):
        nodes = []
        while self.current_token.type != EOF:
            cmp = self.compound_stmt()
            sim = self.simple_stmts()

            if cmp:
                nodes.append(cmp)
            elif sim:
                nodes.append(sim)
            else:
                raise Exception("NONONONONON")

        return StatementListNode(None, nodes)

    def parse(self):
        return self.statements()
