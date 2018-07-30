"""The main turbo interpreter."""


from string import whitespace
import re

from core.stack import Stack
from core.instructions import atoms, metas
from core.utils import base_decode, TokenType, Token
from core.typeinfo import types
import core.io as io


NUMBER = TokenType(0)
STRING = TokenType(1)
BLOCK = TokenType(2)
ATOM = TokenType(3)
META = TokenType(4)

def interpret(code, stack):
    """Interprets Turbo code and places the output in a global variable."""

    try:
        tokens = lex(code)
    except SyntaxError as e:
        raise e
    
    while len(tokens):
        token = tokens.pop()
        if token.type == NUMBER or token.type == STRING:
            stack.push(token.val)
        elif token.type == BLOCK:
            stack.push(Block(token.val))
        elif token.type == ATOM:
            if can_vectorize(token.val, stack):
                vectorize(token.val, stack)
            else:
                type_info = types[token.val]
                coerce_types(stack, type_info)
                atoms[token.val](stack)
        elif token.type == META:
            type_info = types[token.val]
            coerce_types(stack, type_info)
            
            metas[token.val](stack)


class Block:
    def __init__(self, code):
        self.code = code
    
    def run(self, stack):
        interpret(self.code, stack)


def lex(program):
    """Converts a raw turbo program into a list of tokens."""
    program = Stack(reversed(program))  # Reversed so that popping returns the first.
    tokens = Stack()
    
    while len(program):
        if program.top in '0123456789.':
            tstack = Stack()
            while program and program.top in '0123456789.' and program.count('.') <= 1:
                tstack.push(program.pop())
            
            if tstack.top == '.':
                tstack.push('5')  # so that a lone decimal point equals .5
            try:
                num = int(''.join(tstack))
            except ValueError:
                num = float(''.join(tstack))
            tokens.push(Token(NUMBER, num))

        elif program.top == '"':
            program.pop()
            st = take_while(program, lambda x: x not in '">')  # TODO replace with unicode
            if program.top == '"':
                tokens.push(Token(STRING, st))
            else:
                tokens.push(Token(NUMBER, base_decode(st)))
            program.pop()
            # print(st)
            # print(Token(LITERAL, st))
            # print(tokens)
        elif program.top == '{':
            program.pop()
            block = take_while(program, lambda x: x != '}')
            tokens.push(Token(BLOCK, block))
            program.pop()
        elif program.top in whitespace:
            program.pop()
        elif program.top in atoms:
            atom = program.pop()
            if program.top in metas:  # This ensures that atoms become blocks before metas.
                tokens.push(Token(BLOCK, atom))
            else:
                tokens.push(Token(ATOM, atom))
        elif program.top in metas:
            meta = program.pop()
            tokens.push(Token(META, meta))
        else:
            raise SyntaxError(f'Invalid char {program.top}')
    
    return Stack(reversed(tokens))  # So that the first to pop off is the first to execute.


def take_while(stack, cond):
    """Pops characters from stack until cond no longer returns true
    on the top of the stack and return the resulting string"""
    res = []

    while stack and cond(stack.top):
        res.append(stack.pop())
    
    return ''.join(res)


def coerce_types(stack, type_info):
    """Modifies the stack so that the elements on top match the type_info."""
    for element, wanted_type, index in zip(reversed(stack), reversed(type_info), range(len(type_info))):
        if type_of(element) == wanted_type or wanted_type == 'a':
            continue
        actual_type = type_of(element)
        if wanted_type == 'n':
            if actual_type == 's':
                try:
                    stack[index] = int(stack[index])
                except ValueError:
                    raise TypeError('String cannot be coerced to number.')
            elif actual_type == 'b':
                raise TypeError('Block cannot be coerced to number.')
            elif actual_type == 'l':
                raise NotImplementedError() # TODO vectorization. TODO make vectorization work with multi-dim lists...
        elif wanted_type == 's':
            if actual_type == 'n':
                stack[index] == str(stack[index])
            elif actual_type == 'b':
                raise TypeError('Block cannot be coerced to string.')
            elif actual_type == 'l':
                raise NotImplementedError()
        elif wanted_type == 'b':
            if actual_type == 'n':
                raise TypeError('Number cannot be coerced to block.')
            elif actual_type == 's':
                stack[index] = lambda s: interpret(stack[index], s)
            elif actual_type == 'l':
                raise NotImplementedError()
        elif wanted_type == 'l':
            if actual_type == 'n':
                stack[index] = [int(i) for i in str(stack[index]) if i != '.']
            elif actual_type == 's':
                stack[index] = list(stack[index])
            elif actual_type == 'b':
                raise TypeError('Block cannot be coerced to list.')


def type_of(obj):
    """Return the type of an object:
     - n for number
     - s for string
     - b for block
     - l for list."""
    
    if type(obj) is int or type(obj) is float:
        return 'n'
    elif type(obj) is str:
        return 's'
    elif type(obj) is Block:
        return 'b'
    else:
        return 'l'


def vectorize(atom, stack):  # TODO Add type coercion to vectorization.
    type_info = types[atom]
    stack_type_info = ''.join([type_of(x) for x in reversed(stack)][:len(type_info)])
    temp_stack = Stack()

        #  Vectorization needs to occur.
    if len(type_info) == 1:  # atom is a monad.
        for item in stack.pop():
                # This is the list on the stack
            temp_stack.push(item)
            interpret(atom, temp_stack)    
        stack.extend(temp_stack)
    elif len(type_info) == 2:  # atom is a dyad.
        if re.match(r'll', stack_type_info) and re.match(r'[^l][^l]', type_info):
            for item1, item2 in zip(stack.pop(), stack.pop()):
                temp_stack.extend((item1, item2))
                interpret(atom, temp_stack)
            stack.push(list(temp_stack))
        elif re.match(r'[^l]l', stack_type_info) and re.match(r'[^l][^l]', type_info):
            item2 = stack.pop()
            for item1 in stack.pop():
                temp_stack.extend((item1, item2))
                interpret(atom, temp_stack)
            stack.push(list(temp_stack))
        elif re.match(r'l[^l]', stack_type_info) and re.match(r'[^l][^l]', type_info):
            l = stack.pop()
            item1 = stack.pop()
            for item2 in l:
                temp_stack.extend((item1, item2))
                interpret(atom, temp_stack)
            stack.push(list(temp_stack))
            


def can_vectorize(atom, stack):
    type_info = types[atom]
    stack_type_info = map(type_of, list(reversed(stack))[:len(type_info)])

    return 'l' in stack_type_info and 'l' not in type_info
