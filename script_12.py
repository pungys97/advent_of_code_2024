import re
import numpy as np
from scipy.optimize import milp, LinearConstraint

claw_machines = []

claw_machine = dict()
while True:
    try:
        line = input().strip()
        if not line:
            continue
        x, y = re.findall(r"\d+", line)
        if line.startswith("Button A:"):
            claw_machine["a"] = (int(x), int(y))
        elif line.startswith("Button B:"):
            claw_machine["b"] = (int(x), int(y))
        else:
            const = 10_000_000_000_000
            claw_machine["prize"] = (int(x) + const, int(y) + const)
            claw_machines.append(claw_machine)
            claw_machine = dict()
    except EOFError:
        break


def solve_claw_machine(claw_machine):
    a = claw_machine["a"]
    b = claw_machine["b"]
    prize = claw_machine["prize"]
    objective = np.array([3, 1])
    integrality = np.array([1, 1])
    # encode prize[0] <= a[0] * x + b[0] * x <= prize[0]
    # same for prize[1] <= a[1] * x + b[1] * x <= prize[1]

    A = np.array([
        [a[0], b[0]],
        [-a[0], -b[0]],
        [a[1], b[1]],
        [-a[1], -b[1]]
    ])
    b_l = np.array([0, -np.inf, 0, -np.inf])
    b_u = np.array([prize[0], -prize[0], prize[1], -prize[1]])

    constraints = LinearConstraint(A, b_l, b_u)

    res = milp(objective, constraints=constraints, integrality=integrality)
    return res.fun, res.x

tokens = 0
for claw_machine in claw_machines:
    solution, sol_x = solve_claw_machine(claw_machine)
    if solution is None:
        continue
    tokens += solution

print(tokens)