from model.CSP import CSP
from model.Constraint import Constraint, DoubleConstraint


if __name__ == "__main__":
    variables = ["a", "b", "c", "d", "e", "f", "g"]
    domains = {}
    for variable in variables:
        domains[variable] = ["red", "green", "orange"]

    double_constraints = [
        (lambda a, b: a != b, ["a", "c"]),
        (lambda a, b: a != b, ["a", "b"]),
        (lambda a, b: a != b, ["b", "c"]),
        (lambda a, b: a != b, ["b", "c"]),
        (lambda a, b: a != b, ["d", "c"]),
        (lambda a, b: a != b, ["d", "b"]),
        (lambda a, b: a != b, ["d", "e"]),
        (lambda a, b: a != b, ["e", "b"]),
        (lambda a, b: a != b, ["f", "b"]),
        (lambda a, b: a != b, ["f", "e"]),
        (lambda a, b: a != b, ["f", "g"]),
    ]

    
    csp = CSP(
        variables, 
        domains, 
        "Most Constrained Variable", 
        "Least Constrained Value", 
        do_forward_checking=True
    )

    for constraint, variables in double_constraints:
        csp.add_constraint(DoubleConstraint(constraint, variables))

    solution = csp.search()

    if len(solution) == 0:
        print("No solution found!")
    else:
        print(solution)
        print(len(solution))
        print(csp.visited)
