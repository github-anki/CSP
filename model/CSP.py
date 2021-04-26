from abc import ABC, abstractmethod
from typing import Dict, List

from .Constraint import Constraint


class CSP():

    def __init__(
        self, 
        variables: List[str], 
        domains: Dict[str, str], 
        var_heuristic = "Simple Variable", 
        domain_heuristic = "Simple Value",
        do_forward_checking = False
    ):
        self.variables = variables 
        self.domains = domains 
        self.constraints: Dict[str, List[Constraint]] = {}
        self.heuristic_select_variable = self.heuristic_mapper(var_heuristic)
        self.heuristic_select_domain = self.heuristic_mapper(domain_heuristic)

        # Forward checking
        self.do_forward_checking = do_forward_checking
        self.pruned = {d: [] for d in domains.keys()}

        # Results and statistics
        self.visited = 0

        for variable in self.variables:
            self.constraints[variable] = []
            if variable not in self.domains:
                raise ValueError("Variable should have a domain.")
    
    def heuristic_mapper(self, heuristic):
        if heuristic == "Simple Variable":
            return self.simple_variable
        elif heuristic == "Most Constrained Variable":
            return self.most_constrained_variable
        if heuristic == "Simple Value":
            return self.simple_value
        elif heuristic == "Least Constrained Value":
            return self.least_constrained_value
    
    def get_neighbours(self):
        neighbours = {}

        for var in self.variables:
            var_neighbours = []

            for cst in self.constraints[var]:
                for v in cst.variables:
                    if v != var:
                        var_neighbours.append(v)

            var_neighbours = list(set(var_neighbours))
            neighbours[var] = var_neighbours

        return neighbours

    def add_constraint(self, constraint):
        for variable in constraint.variables:
            if variable not in self.variables:
                raise ValueError("Variable in constraint not in CSP")
            else:
                self.constraints[variable].append(constraint)
    
    def consistent(self, variable, assignment):
        for constraint in self.constraints[variable]:
            if not constraint.satisfied(assignment):
                return False
        return True

    def forward_checking(self, variable, value, assignment={}):
        neighbours = self.get_neighbours()
        
        for neighbour in neighbours[variable]:
            if neighbour not in assignment:
                if value in self.domains[neighbour]:
                    self.domains[neighbour].remove(value)
                    self.pruned[variable].append((neighbour, value))

    def most_constrained_variable(self, assignment):
        unassigned = [v for v in self.variables if v not in assignment]
        return min(unassigned, key=lambda var: len(self.domains[var]))

    def simple_variable(self, assignment):
        unassigned = [v for v in self.variables if v not in assignment]
        return unassigned[0]

    def least_constrained_value(self, first):
        if len(self.domains[first]) == 1:
            return self.domains[first]
        return sorted(self.domains[first], key=lambda val: self.conflicts(self, first, self.domains))
    
    def simple_value(self, first):
       return self.domains[first]

    @staticmethod
    def conflicts(csp, var, val):
        count = 0
        neighbours = csp.get_neighbours()
        for n in neighbours:
            if len(csp.domains[n]) > 1 and val in csp.domains[n]:
                count += 1
        return count

    def backtracking_search(self, assignment = {}):
        self.visited += 1

        if len(assignment) == 0:
            self.results_ = []

        if len(assignment) == len(self.variables):
            self.results_.append(assignment)
            return assignment

        first = self.heuristic_select_variable(assignment)

        for value in self.heuristic_select_domain(first):
            #local_assignment = assignment.copy()
            assignment[first] = value
            
            if self.consistent(first, assignment):
                self.forward_check(first, value, assignment)
                result = self.backtracking_search(assignment)

                if result is not None:
                    return result
                
                self.restore_domains(first, assignment)

        return None


    def forward_check(self, variable, value, assignment):
        if self.do_forward_checking:
            self.forward_checking(variable, value, assignment)


    def restore_domains(self, variable, assignment):
        if self.do_forward_checking:
            if variable in assignment:
                for domain, value in self.pruned[variable]:
                    self.domains[domain].append(value)

                self.pruned[variable] = []
                del assignment[variable]

    def search(self):
        self.backtracking_search()
        return self.results_
