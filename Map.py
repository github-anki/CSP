import time
from itertools import product
from tqdm import tqdm

import pandas as pd

from model.CSP import CSP
from model.Constraint import DoubleConstraint

from utils.map_generator import Map


def perform_experiment(
        num_of_points,
        k=3,
        var_heuristic="Simple Variable",
        domain_heuristic="Simple Value",
        do_forward_checking=False
):
    mapa = Map()
    mapa.generate_points(num_of_points)
    mapa.connect_points()

    dom = ["red", "green", "orange"] if k == 3 else ["red", "green", "blue", "orange"]

    variables = [p.name for p in mapa.points]
    domains = {}
    for variable in variables:
        domains[variable] = dom

    double_constraints = [
        (lambda a, b: a != b, [line.point1.name, line.point2.name]) for line in mapa.lines
    ]

    csp = CSP(
        variables,
        domains,
        var_heuristic=var_heuristic,
        domain_heuristic=domain_heuristic,
        do_forward_checking=do_forward_checking
    )

    for constraint, variables in double_constraints:
        csp.add_constraint(DoubleConstraint(constraint, variables))

    start = time.time()
    solution = csp.search()
    return (len(solution), csp.visited, time.time() - start)


if __name__ == "__main__":
    var_heuristics = [
        "Simple Variable",
        "Most Constrained Variable"
    ]
    domain_heuristics = [
        "Simple Value",
        "Least Constrained Value"
    ]
    ks = [
        3,
        4
    ]
    fw_chs = [
        # True,
        False
    ]
    num_nodes = list(range(3, 14))
    n_iter = list(range(5))

    results = []

    for num_node, k, var_heuristic, domain_heuristic, fw_ch, i in tqdm(
            product(num_nodes, ks, var_heuristics, domain_heuristics, fw_chs, n_iter)):
        results.append((
            num_node,
            k,
            var_heuristic,
            domain_heuristic,
            fw_ch,
            i,
            *perform_experiment(
                num_of_points=num_node,
                k=k,
                var_heuristic=var_heuristic,
                domain_heuristic=domain_heuristic,
                do_forward_checking=fw_ch
            )
        ))

    df = pd.DataFrame(
        results,
        columns=[
            "num_node",
            "k",
            "var_heuristic",
            "domain_heuristic",
            "forward_checking",
            "iteration",
            "solution",
            "nodes_visited",
            "time"
        ]
    )
    df.to_csv("results/map_experiment_results.csv", index=False)
