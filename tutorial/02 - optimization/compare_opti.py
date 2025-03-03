import robosandbox as rsb
from robosandbox.performance.WorkSpace import WorkSpace
from robosandbox.optimization.opti_scipy import Opti
from robosandbox.optimization.opti_scipy import ExternalFunctionExpression
import numpy as np
from scipy.optimize import minimize

def objective_global_indice(alpha2, alpha3, alpha4, method):
    robot = rsb.models.DH.Generic.GenericFour(alpha=[alpha2, alpha3, alpha4, 0])
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

# Conversion from degrees to radians for alpha bounds
lb = np.deg2rad(0)  # Lower bound in radians
ub = np.deg2rad(90)   # Upper bound in radians

# Define the bounds and initial guess for the optimization
initial_guess = [(lb + ub) / 2, (lb + ub) / 2, (lb + ub) / 2]  # Midpoint for the initial guess

# Define the bounds as a list of tuples (lower, upper)
bounds = [(lb, ub), (lb, ub), (lb, ub)]

# Objective function for scipy.optimize (must return a scalar)
def obj_func(x):
    alpha2, alpha3, alpha4 = x
    return -objective_global_indice(alpha2, alpha3, alpha4, method='invcondition')

options = {
    'maxiter': 1000,  # Maximum number of iterations
    'disp': True
}

# Perform the optimization using scipy.optimize.minimize
result = minimize(obj_func, [np.pi/4, 0, np.pi/8], bounds=bounds, method='SLSQP', options=options)

# Print the results
if result.success:
    print("Optimization successful!")
    print("Optimal values for alpha2, alpha3, and alpha4:", result.x)
    print("Optimal value of the objective function:", result.fun)
else:
    print("Optimization failed:", result.message)

print(np.rad2deg(result.x[0]), np.rad2deg(result.x[1]), np.rad2deg(result.x[2]))
