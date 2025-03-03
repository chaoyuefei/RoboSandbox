import robosandbox as rsb
from robosandbox.performance.WorkSpace import WorkSpace
from robosandbox.optimization.opti_scipy import Opti
from robosandbox.optimization.opti_scipy import ExternalFunctionExpression
import numpy as np

# Define the Objective Function
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
lb = np.deg2rad(0)    # Lower bound in radians
ub = np.deg2rad(90)   # Upper bound in radians

# Initialize the Optimization Environment
opti = Opti()

# Define Variables with Initial Guesses and Bounds
initial_guess = (lb + ub) / 2  # Midpoint for the initial guess

alpha2 = opti.variable(init_guess=np.pi/4, name='alpha2', bounds=(lb, ub))
alpha3 = opti.variable(init_guess=0, name='alpha3', bounds=(lb, ub))
alpha4 = opti.variable(init_guess=np.pi/8, name='alpha4', bounds=(lb, ub))

# Define the Objective Expression Using ExternalFunctionExpression
objective_expr = ExternalFunctionExpression(
    func=lambda a2, a3, a4: -objective_global_indice(a2, a3, a4, method='invcondition'),
    variables=[alpha2, alpha3, alpha4]
)

def obj_func(x):
    alpha2, alpha3, alpha4 = x
    return -objective_global_indice(alpha2, alpha3, alpha4, method='invcondition')

# f = obj_func([alpha2, alpha3, alpha4])
# Set the Objective for Minimization
# opti.minimize(f)

# (Optional) Define Additional Constraints if Needed
# Example: Ensure that alpha2 + alpha3 + alpha4 <= some value
# constraint_expr = alpha2 + alpha3 + alpha4 <= np.deg2rad(180)
# opti.subject_to(constraint_expr)
#
opti.minimize(objective_expr)


# Solve the Optimization Problem
solution = opti.solve()

# Display the Results
if solution.success():
    optimized_alpha2 = solution(alpha2)
    optimized_alpha3 = solution(alpha3)
    optimized_alpha4 = solution(alpha4)
    print("Optimization was successful!")
    print(f"Optimal alpha2: {np.rad2deg(optimized_alpha2):.2f} degrees")
    print(f"Optimal alpha3: {np.rad2deg(optimized_alpha3):.2f} degrees")
    print(f"Optimal alpha4: {np.rad2deg(optimized_alpha4):.2f} degrees")
    print(f"Optimal Objective Value: {solution.result.fun}")
else:
    print("Optimization failed:", solution.message())
