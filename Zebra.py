from model.CSP import CSP
from model.Constraint import Constraint, SingleConstraint, DoubleConstraint, MultipleConstraint

if __name__ == "__main__":
    colors = ["red", "white", "green", "yellow", "blue"]
    nationalities = ["brit", "swede", "dane", "norwegian", "german"]
    drinks = ["tea", "coffee", "milk", "beer", "water"]
    smokes = ["light", "bez filtra", "pipe", "menthol", "cigar"]
    pets = ["dogs", "birds", "cats", "horses", "fish"]

    variables = colors + nationalities + drinks + smokes + pets
    domains ={}

    for var in variables:
        domains[var] = list(range(1, 6))

    house = [1, 2, 3, 4, 5]

    single_constraints = [
        (lambda a: a == 1, "norwegian"),
        (lambda a: a == 3, "milk")
    ]

    double_constraints = [
        (lambda a, b: a == b, ["brit", "red"]),
        (lambda a, b: a - b == -1, ["green", "white"]),
        (lambda a, b: a == b, ["dane", "tea"]),
        (lambda a, b: abs(a-b) == 1, ["light", "cats"]),
        (lambda a, b: a == b, ["yellow", "cigar"]),
        (lambda a, b: a == b, ["german", "pipe"]),
        (lambda a, b: abs(a-b) == 1, ["light", "water"]),
        (lambda a, b: a == b, ["bez filtra", "birds"]),
        (lambda a, b: a == b, ["swede", "dogs"]),
        (lambda a, b: abs(a-b) == 1, ["norwegian", "blue"]),
        (lambda a, b: abs(a-b) == 1, ["horses", "yellow"]),
        (lambda a, b: a == b, ["menthol", "beer"]),
        (lambda a, b: a == b, ["green", "coffee"])
    ]

    multiple_constraints = [
        (lambda a, b: a != b, nationalities),
        (lambda a, b: a != b, colors),
        (lambda a, b: a != b, smokes),
        (lambda a, b: a != b, drinks),
        (lambda a, b: a != b, pets),
    ]

    csp = CSP(
        variables,
        domains, 
        "Most Constrained Variable",
        "Least Constrained Value",
        do_forward_checking=True
    )

    for constraint, domain in single_constraints:
        csp.add_constraint(SingleConstraint(constraint, domain))

    for constraint, domain in double_constraints:
        csp.add_constraint(DoubleConstraint(constraint, domain))

    for constraint, domain in multiple_constraints:
        csp.add_constraint(MultipleConstraint(constraint, domain))

    solution = csp.search()

    if len(solution) == 0:
        print("No solution found!")
    else:
        print(solution)
    
    print(len(solution))
    print(csp.visited)

    correct_solution = {
        'red': 3,
        'white': 5,
        'green': 4,
        'yellow': 1, 
        'blue': 2,
        'norwegian': 1,
        'swede': 5,
        'dane': 2,
        'german': 4,
        'tea': 2,
        'coffee': 4,
        'milk': 3,
        'beer': 5,
        'water': 1,
        'light': None,
        'pipe': None,
        'menthol': None,
        'cigar': None,
        'bez filtra': None,
        'dogs': 5,
        'birds': 3,
        'horses': 2,
        'cats': 1,
        'fish': 4
    }
