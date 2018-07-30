"""The module containing the dicts of atoms and metas and their implementations.
Each function in these dictionaries should be function from stack to stack.
Data types will be given already converted into the types required.

Metas will have callables pushed on to the stack for them."""


from core.utils import Stack
import core.io as io

def run_block(s):
    block = s.pop()
    num = s.pop()
    for _ in range(num):
        block.run(s)


def debug(s):
    io.output_buf += str(s.pop())


def form_list(s):
    val = list(s)
    s.clear()
    s.push(val)


atoms = {
    '+': lambda s: s.push(s.pop() + s.pop()),
    '-': lambda s: s.push(-s.pop() + s.pop()),
    '*': lambda s: s.push(s.pop() * s.pop()),
    '/': lambda s: s.push(1/s.pop() * s.pop()),
    '%': lambda s: s.push(s.pop() % s.pop()),
    '=': lambda s: s.push(1 if s.pop() == s.pop() else 0),
    '<': lambda s: s.push(1 if s.pop() < s.pop() else 0),
    '>': lambda s: s.push(1 if s.pop() > s.pop() else 0),
    'd': debug,
    'l': form_list,
    'f': lambda s: s.push([s.pop(), s.pop(), s.pop(), s.pop()][::-1]),
}

metas = {
    '!': run_block,
}
