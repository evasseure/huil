from src.ast import FunctionNode, NumNode, StringNode
from src.token import *
from rich import print


class NodeVisitor:
    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name, self.unhandled_visit)
        return visitor(node)

    def unhandled_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser, shared_scope={}):
        self.parser = parser
        self.global_scope = {
            "print": FunctionNode(None, "print", ["text"], []),
            "input": FunctionNode(None, "input", ["text"], []),
            **shared_scope,
        }

    def visit_BinaryOpNode(self, node):
        if node.token.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.token.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.token.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.token.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.token.type == MOD:
            return self.visit(node.left) % self.visit(node.right)
        elif node.token.type == AND:
            return self.visit(node.left) and self.visit(node.right)
        elif node.token.type == OR:
            return self.visit(node.left) or self.visit(node.right)
        elif node.token.type == INFEQUAL:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.token.type == SUPEQUAL:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.token.type == INF:
            return self.visit(node.left) < self.visit(node.right)
        elif node.token.type == SUP:
            return self.visit(node.left) > self.visit(node.right)
        elif node.token.type == EQUAL:
            return self.visit(node.left) == self.visit(node.right)

    def visit_UnaryOpNode(self, node):
        if node.token.type == PLUS:
            return self.visit(node.value)
        elif node.token.type == MINUS:
            return -self.visit(node.value)

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
        function = self.global_scope.get(node.id)
        if function == None:
            raise NameError("Undeclared function: " + node.id)

        if function.id == "print":
            print(self.visit(node.arguments[0]))
            return

        if function.id == "input":
            # TODO It's probably the users responsability to transform it to int ou float
            text = input(self.visit(node.arguments[0]))
            # https://nbviewer.org/github/rasbt/One-Python-benchmark-per-day/blob/master/ipython_nbs/day6_string_is_number.ipynb?create=1
            if text.isdigit():
                return self.visit(NumNode(None, int(text)))
            if text.replace(".", "", 1).isdigit():
                return self.visit(NumNode(None, float(text)))
            return self.visit(StringNode(None, text))

        # We save the previous state before we start adding scoped variables
        previous_state = self.global_scope

        for i in range(len(function.arguments)):
            self.global_scope[function.arguments[i]] = self.visit(node.arguments[i])

        returned = self.visit(
            self.global_scope[node.id].statements,
        )
        self.global_scope = previous_state
        return returned

    def visit_DeclarationNode(self, node):
        if self.global_scope.get(node.id) is not None:
            raise NameError(f"Variable already declared: {node.id} at (l{node.token.line}:c{node.token.column})")
        self.global_scope[node.id] = node.value

    def visit_AssignmentNode(self, node):
        if self.global_scope.get(node.id) is None:
            raise NameError(f"Undeclared variable: {node.id} at (l{node.token.line}:c{node.token.column})")
        self.global_scope[node.id] = node.value

    def visit_VariableNode(self, node):
        if self.global_scope.get(node.id) is None:
            raise NameError(f"Undeclared variable: {node.id} at (l{node.token.line}:c{node.token.column})")
        return self.visit(self.global_scope[node.id])

    def visit_FunctionNode(self, node):
        self.global_scope[node.id] = node

    def visit_StatementListNode(self, node):
        last_value = None
        for statement in node.statements:
            # print(self.global_scope)
            last_value = self.visit(statement)
        return last_value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
