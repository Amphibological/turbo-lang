"""A simple stack."""


class Stack(list):
    push = list.append

    @property
    def top(self):
        return self[-1] if self else None
    
    @top.setter
    def top(self, val):
        self[-1] = val
