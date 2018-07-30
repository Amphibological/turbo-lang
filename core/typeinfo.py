"""Contains the type signatures for all the atoms and metas.

Each type signature consists of a number of characters:
 - n for number,
 - l for list,
 - s for string,
 - b for block, and
 - a for any of the above.

The rightmost value is the first off the stack (i.e types are pushed onto the stack left-to-right.) """

types = {
    '+': 'nn',
    '-': 'nn',
    '*': 'nn',
    '/': 'nn',
    '%': 'nn',
    '=': 'aa',
    '<': 'aa',
    '>': 'aa',
    'd': 'a',
    'l': 'a',
    '!': 'nb',
    'f': 'aaaa',
}
