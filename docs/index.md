# Turbo Docs

_Welcome to the Turbo documentation. Since Turbo is currently in beta, this site is very much a work in progress. Nevertheless, feel free to look around. Don't worry, there's more to come soon! :)_



Turbo is a language designed for code golf. Code golf is a specific type of programming challenge wherein the goal is to accomplish a specific goal in as few bytes of code as possible. To that end, Turbo has a large number of single-byte builtins to accomplish common tasks.



Turbo also uses a stack-based model, which means all of its instructions revolve around a stack.

A stack is a LIFO (last in, first out queue). To illustrate what that means, think about a stack of heavy books. When you want to add a book, you put it on top of the stack. To remove a book, you take the topmost book off. These concepts (adding and removing a single book) are referred to as _pushing_ and _popping_ respectively. So, if I have a stack of numbers like this:

```
1 < top of stack
2
3 < bottom of stack
```

and I _push_ a 4, the stack would look like this:

```
4 < top of stack
1
2
3 < bottom of stack
```

If I then _popped_ off two numbers (the 4 and the 1), the result is this:

```
2 < top of stack
3 < bottom of stack
```

In Turbo, (almost) every single instruction either pushes or pops (or both) to one global stack. For example, the `+` instruction, which adds two numbers, will pop two numbers from the global stack, add them and then push the result. From now on the global stack will be referred to simply as __the stack__.

Understanding the stack is the one of the most important aspects of programming in Turbo, so make sure you fully understand this before moving on.