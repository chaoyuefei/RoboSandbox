import robosandbox as rsb
from robosandbox.performance.WorkSpace import WorkSpace
from robosandbox.optimization.opti_scipy import Opti
import numpy as np
from math import pi


def objective_global_indice(
    linklengths=[0.4] * 4, alpha=[pi / 2, 0, 0, 0], method="yoshikawa"
):
    robot = rsb.models.DH.Generic.GenericFour(linklengths=linklengths, alpha=alpha)
    ws = WorkSpace(robot=robot)
    G = ws.iter_calc_global_indice(
        initial_samples=3000,
        batch_ratio=0.1,
        error_tolerance_percentage=1e-3,
        method=method,
        axes="all",
        max_samples=30000,
    )
    return G


if __name__ == "__main__":
    (lb, ub) = (np.deg2rad(0), np.deg2rad(180))

    opti = Opti()

    alpha2 = opti.variable(init_guess=0, name="alpha2", bounds=(lb, ub))
    alpha3 = opti.variable(init_guess=0, name="alpha3", bounds=(lb, ub))
    alpha4 = opti.variable(init_guess=0, name="alpha4", bounds=(lb, ub))
    alphaee = opti.variable(init_guess=0, name="alphaee", bounds=(lb, ub))

    obj = opti.external_func(
        func=lambda a3, a4: objective_global_indice(
            linklengths=[0.4] * 4, alpha=[pi / 2, a3, a4, 0], method="invcondition"
        ),
        variables=[alpha3, alpha4],
    )

    opti.maximize(obj)
    sol = opti.solve(method="Powell")

    if sol.success():
        # optimized_alpha2 = solution(alpha2)
        optimized_alpha3 = sol(alpha3)
        optimized_alpha4 = sol(alpha4)
        print("Optimization was successful!")
        # print(f"Optimal alpha2: {np.rad2deg(optimized_alpha2):.2f} degrees")
        print(f"Optimal alpha3: {np.rad2deg(optimized_alpha3):.2f} degrees")
        print(f"Optimal alpha4: {np.rad2deg(optimized_alpha4):.2f} degrees")
        print(f"Optimal Objective Value: {sol.result.fun}")
    else:
        print("Optimization failed:", sol.message())
