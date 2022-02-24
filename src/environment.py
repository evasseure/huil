from typing import Any, Dict, Optional


class Environment:
    parent: "Environment" = None
    values: Dict[str, Any]

    def __init__(self, parent: Optional["Environment"] = None) -> None:
        if parent is not None:
            self.parent = parent
        self.values = {}

    def declare(self, key: str, value: Any = None) -> None:
        if key in self.values:
            raise NameError(f"Variable already declared: {key}")
        self.values[key] = value

    def set(self, key: str, value: Any) -> None:
        if key in self.values:
            self.values[key] = value
        elif self.parent is not None:
            self.parent.set(key, value)

        raise NameError(f"Undeclared variable: {key}")

    def get(self, key: str) -> Any:
        if key in self.values:
            return self.values[key]

        if self.parent is not None:
            return self.parent.get(key)

        raise NameError(f"Undeclared variable: {key}")
