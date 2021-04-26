from abc import ABC, abstractmethod
from itertools import combinations
from typing import Callable, List

class Constraint(ABC):
    def __init__(self, variables):
        self.variables = variables

    @abstractmethod
    def satisfied(self, assignment):
        ...

class SingleConstraint(Constraint):
    def __init__(self, constraint: Callable, var1: str):
        super().__init__([var1])
        self.var1 = var1
        self.constraint = constraint

    def satisfied(self, assignment):
        if self.var1 not in assignment:
            return True
        return self.constraint(assignment[self.var1])

class DoubleConstraint(Constraint):
    def __init__(self, constraint: Callable, variables: List[str]):
        super().__init__(variables)
        self.var1 = variables[0]
        self.var2 = variables[1]
        self.constraint = constraint

    def satisfied(self, assignment):
        if self.var1 not in assignment or self.var2 not in assignment:
            return True
        return self.constraint(assignment[self.var1], assignment[self.var2])

class MultipleConstraint(Constraint):
    def __init__(self, constraint: Callable, variables):
        super().__init__(variables)
        self.constraint = constraint

    def satisfied(self, assignment):
        for var1, var2 in combinations(self.variables, 2):
            if var1 in assignment and var2 in assignment:
                if not self.constraint(assignment[var1], assignment[var2]):
                    return False
        return True 
