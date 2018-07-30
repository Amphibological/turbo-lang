"""General utilities."""

from collections import namedtuple

Token = namedtuple('Token', ('type', 'val'))

TOKEN_TYPES = ['NUMBER', 'STRING', 'BLOCK', 'ATOM', 'META']

def base_decode(s):
    """Decode a base-250 encoded string into a number."""
    return None


class TokenType(int):
    def __str__(self):
        return TOKEN_TYPES[self]

    def __repr__(self):
        return self.__str__()


class Stack(list):
    push = list.append

    @property
    def top(self):
        return self[-1] if self else None
    
    @top.setter
    def top(self, val):
        self[-1] = val
