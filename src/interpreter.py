from src.ast import FunctionNode, NumNode, StringNode
from src.environment import Environment
from src.token import *
from rich import print
import readline  # Necessary to have a nice python input()


class RuntimeException(Exception):
    pass


class TypeError(RuntimeException):
    def __init__(self, message):
        super().__init__(message)


class NodeVisitor:
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.unhandled_visit)
        return visitor(node)

    def unhandled_visit(self, node):
        raise Exception("InterpreterError: No visit_{} method".format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self):
        self.env = Environment()

    def visit_BinaryOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.token.type in (AND, OR):
            if (type(left) != bool) or (type(right) != bool):
                raise TypeError(f"Can't do {node.left.token.type} {node.token.value} {node.right.token.type}")

            if node.token.type == AND:
                return left and right
            elif node.token.type == OR:
                return left or right

        if (type(left) != int and type(left) != float) or (type(right) != int and type(right) != float):
            raise TypeError(f"Can't do {node.left.token.type} {node.token.value} {node.right.token.type}")

        if node.token.type == PLUS:
            return left + right
        elif node.token.type == MINUS:
            return left - right
        elif node.token.type == MUL:
            return left * right
        elif node.token.type == DIV:
            return left / right
        elif node.token.type == MOD:
            return left % right
        elif node.token.type == SUPEQUAL:
            return left >= right
        elif node.token.type == INF:
            return left < right
        elif node.token.type == SUP:
            return left > right
        elif node.token.type == EQUAL:
            return left == right
        elif node.token.type == NOTEQUAL:
            return left != right
        elif node.token.type == INFEQUAL:
            return left <= right

    def visit_UnaryOpNode(self, node):
        value = self.visit(node.value)

        if type(value) != bool:
            raise TypeError(f"Can't do {node.token.value} {value}")

        if node.token.type == NOT:
            return not value

        if type(value) != int and type(value) != float:
            raise TypeError(f"Can't do {node.token.value} {value}")

        if node.token.type == PLUS:
            return value
        elif node.token.type == MINUS:
            return -value

    def visit_NilNode(self, node):
        return None

    def visit_NumNode(self, node):
        return node.value

    def visit_BooleanNode(self, node):
        return node.value

    def visit_StringNode(self, node):
        return node.value

    def visit_MatchNode(self, node):
        value = self.visit(node.factor)

        for match in node.matches:
            if match[0].value == "*":
                return self.visit(match[1])
            if self.visit(match[0]) == value:
                return self.visit(match[1])
        return None

    def visit_FunctionCallNode(self, node):
        function = self.env.get(node.id)

        if function.id == "print":
            print(self.visit(node.arguments[0]))
            return

        if function.id == "input":
            # TODO It's probably the users responsability to transform it to int ou float
            if len(node.arguments) > 0:
                text = input(self.visit(node.arguments[0]))
            else:
                text = input()
            # https://nbviewer.org/github/rasbt/One-Python-benchmark-per-day/blob/master/ipython_nbs/day6_string_is_number.ipynb?create=1
            if text.isdigit():
                return self.visit(NumNode(Token(INTEGER, text, 0, 0)))
            if text.replace(".", "", 1).isdigit():
                return self.visit(NumNode(Token(FLOAT, text, 0, 0)))
            return self.visit(StringNode(None, text))

        # We save the previous state before we start adding scoped variables
        previous_state = self.env
        self.env = Environment(previous_state)

        fn_args_count = len(function.arguments)
        fn_call_args_count = len(node.arguments)
        if fn_args_count > fn_call_args_count:
            raise TypeError(f"Missing arguments {function.arguments[fn_args_count-fn_call_args_count-1:]}")
        # We son't care about extra fn call arguments

        for i in range(fn_args_count):
            self.env.declare(function.arguments[i], self.visit(node.arguments[i]))

        returned = self.visit(
            self.env.get(node.id).statements,
        )
        self.env = previous_state
        return returned

    def visit_IfThenElseNode(self, node):
        for i in range(len(node.conditions)):
            res = self.visit(node.conditions[i])
            if res:
                self.visit(node.truthy_statements[i])

        if node.else_statements:
            self.visit(node.else_statements)

    def visit_WhileNode(self, node):
        while self.visit(node.condition):
            self.visit(node.statements)

    def visit_DeclarationNode(self, node):
        self.env.declare(node.id, self.visit(node.value))

    def visit_AssignmentNode(self, node):
        self.env.set(node.id, self.visit(node.value))

    def visit_VariableNode(self, node):
        return self.env.get(node.id)

    def visit_ReturnNode(self, node):
        return self.visit(node.value)

    def visit_FunctionNode(self, node):
        self.env.declare(node.id, node)

    def visit_StatementListNode(self, node):
        for statement in node.statements:
            if statement.token.type == RETURN:
                return self.visit(statement)
            self.visit(statement)

    def interpret(self, parser):
        tree = parser.parse()
        self.visit(tree)
