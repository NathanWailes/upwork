Write a Python program that emulates the behavior of the Prolog "family.pro" program attached:

You will need to only emulate queries that have at all but one of the arguments known.
This means that for something like

?-cousin_of('Marie',Who).

you will have a query like:


> list(cousin_of('Marie'))



> for Who in cousin_of('Marie') : print(Who)


You can uses "yield" to return multiple answers, as needed.