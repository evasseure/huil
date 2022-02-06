import operator as op


def create_env():
    "An environment with some Scheme standard procedures."
    env = {}
    env.update(
        {
            "+": op.add,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv,
            ">": op.gt,
            "<": op.lt,
            ">=": op.ge,
            "<=": op.le,
            "==": op.eq,
            "%": op.mod,
        }
    )
    return env
