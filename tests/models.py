from collections import namedtuple
from enum import Enum

# === User-defined class ===
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hello, I'm {self.name} and I'm {self.age} years old."

    def __eq__(self, other):
        return isinstance(other, Person) and self.name == other.name and self.age == other.age

# === namedtuple ===
Point = namedtuple("Point", ["x", "y"])

# === Enum ===
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3