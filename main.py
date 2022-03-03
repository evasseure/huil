from rich import print
import sys
from src.environment import NameErrorException

from src.interpreter import Interpreter, RuntimeException
from src.lexer import Lexer
from src.parser import Parser
import os
import readline

histfile_size = 1000
histfile = "./.history"


def run(code):
    lexer = Lexer(code)
    parser = Parser(lexer)
    # print(parser.parse())
    interpreter = Interpreter()
    interpreter.interpret(parser)


def test_file(filename):
    with open(f"./examples/{filename}") as f:
        run(f.read())


def repl():
    # Initializes the REPL history
    if not os.path.exists(histfile):
        with open(histfile, "w") as _:
            pass
    readline.read_history_file(histfile)
    readline.set_history_length(histfile_size)

    interpreter = Interpreter()
    while True:
        try:
            code = input("hul> ")
            if code == "print_scope()":
                print(interpreter.env.values)
                continue
            if not code:
                continue
            lexer = Lexer(code)
            parser = Parser(lexer)
            result = interpreter.interpret(parser)
            print(result)

            readline.write_history_file(histfile)
        except EOFError:
            break
        except KeyboardInterrupt:
            break
        except RuntimeException as e:
            print(e)
        except NameErrorException as e:
            print(e)
        except Exception as e:
            # print(e)
            raise (e)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        repl()

    elif sys.argv[1] == "-t":
        print("Running tests...")
        print("...jk")

    elif sys.argv[1] == "-f" and len(sys.argv) == 3:
        test_file(sys.argv[2])
