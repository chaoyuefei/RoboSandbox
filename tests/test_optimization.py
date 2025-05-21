import unittest
import robosandbox as rsb
import numpy as np


# class TestRobotOptimization(unittest.TestCase):
#     def test_opti(self):
#         """
#         Test the optimization functionality.
#         """
#         # Create optimization problem
#         opti = rsb.optimization.opti_scipy.Opti()
#         # Define variables with initial guesses and bounds
#         x = opti.variable(init_guess=5, name="x")
#         y = opti.variable(init_guess=0, name="y")

#         # Define an objective function: f = x^2 + y^2
#         f = x**2 + y**2
#         opti.minimize(f)

#         # Add constraints: x > 3 and y >= 2
#         opti.subject_to(x > 3)
#         opti.subject_to(y >= 2)
#         opti.subject_to(x + y <= 7)

#         # Solve the optimization problem
#         sol = opti.solve()

#         # Check the solution
#         self.assertTrue(sol.success())
#         self.assertAlmostEqual(sol(x), 3, places=2)
#         self.assertAlmostEqual(sol(y), 2, places=2)
#         self.assertAlmostEquals(sol.result.fun, 13, places=2)

#     def test_opti_01(self):
#         """
#         Test the optimization functionality.
#         """
#         # Create optimization problem
#         opti = rsb.optimization.opti_scipy.Opti()
#         # Define variables with bounds
#         x = opti.variable(name="x", bounds=(0, 5), init_guess=1)
#         y = opti.variable(name="y", bounds=(0, 5), init_guess=1)

#         # Define objective function
#         obj = (x - 2) ** 2 + (y - 1) ** 2

#         # Add constraint
#         opti.subject_to(x + y >= 3)

#         # Solve without sweep to verify
#         opti.minimize(obj)
#         sol = opti.solve()

#         self.assertTrue(sol.success())
#         self.assertAlmostEqual(sol(x), 2, places=2)
#         self.assertAlmostEqual(sol(y), 1, places=2)
#         self.assertAlmostEqual(sol.result.fun, 0, places=2)

#     def test_opti_external_function(self):
#         """
#         Test the optimization functionality with an external function.
#         """
#         # Create optimization problem
#         opti = rsb.optimization.opti_scipy.Opti()
#         # Define variables with bounds
#         x = opti.variable(name="x", bounds=(0, 5), init_guess=1)
#         y = opti.variable(name="y", bounds=(0, 5), init_guess=1)

#         # Define objective function
#         # obj = (x - 2) ** 2 + (y - 1) ** 2
#         def obj_func(x, y, a, b):
#             return (x - 2) ** 2 + (y - 1) ** 2 + a + b

#         # Add constraint
#         opti.subject_to(x + y >= 3)

#         obj = opti.external_func(
#             func=lambda x_var, y_var: obj_func(x_var, y_var, 1, 1),
#             variables=[x, y],
#         )

#         # Solve without sweep to verify
#         opti.minimize(obj)
#         sol = opti.solve()

#         self.assertTrue(sol.success())
#         self.assertAlmostEqual(sol(x), 2, places=2)
#         self.assertAlmostEqual(sol(y), 1, places=2)
#         self.assertAlmostEqual(sol.result.fun, 2, places=2)

#     # def test_opti_sweep(self):
#     #     # Create a simple optimization problem
#     #     opti = rsb.optimization.opti_scipy.Opti()

#     #     # Define variables
#     #     x = opti.variable(init_guess=0, name="x", bounds=(-5, 5))
#     #     y = opti.variable(init_guess=0, name="y", bounds=(-5, 5))

#     #     # Define objective function: a simple quadratic
#     #     obj = x**2 + y**2 - 2 * x * y + 2 * x + 3 * y
#     #     # Analytical minimum at x=-1, y=-2 with value -3

#     #     # Set objective for optimization
#     #     opti.minimize(obj)

#     #     # Set the same objective for sweeping
#     #     opti.sweep(obj)

#     #     # Define the parameter sweep with a coarse grid
#     #     sweep_vars = {
#     #         "x": np.linspace(-2, 0, 3),  # -2, -1, 0
#     #         "y": np.linspace(-3, -1, 3),  # -3, -2, -1
#     #     }

#     #     # Run the sweep
#     #     results = opti.solve_sweep(sweep_vars)

#     #     # Print results
#     #     print("\nSweep results:")
#     #     print(results.dataframe)

#     #     # Check if the best result is close to the analytical solution
#     #     best = results.get_optimal_point(minimize=True)
#     #     print("\nBest result:")
#     #     print(f"x = {best['x']}, y = {best['y']}, objective = {best['objective']}")
#     #     print("Expected analytical solution: x = -1, y = -2, objective = -3")

#     #     return results
#     def test_sweeper(self):
#         def objective_function(alpha3, alpha4, method="invcondition", axes="all"):
#             """Objective function to evaluate robot performance for given alpha values"""
#             robot = rsb.models.DH.Generic.GenericFour(
#                 alpha=[np.pi / 2, alpha3, alpha4, 0]
#             )
#             ws = rsb.performance.workspace.WorkSpace(robot=robot)
#             G = ws.global_indice(
#                 initial_samples=3000,
#                 batch_ratio=0.1,
#                 error_tolerance_percentage=1e-3,
#                 method=method,
#                 axes=axes,
#                 max_samples=30000,
#             )
#             return G

#         # Create parameter sweeper
#         sweeper = rsb.optimization.sweeper.ParameterSweeper(
#             objective_function=objective_function,
#             save_path=None,
#         )

#         # Define parameter ranges
#         alpha3_list = np.linspace(0, np.pi / 2, 2)
#         alpha4_list = np.linspace(0, np.pi / 2, 2)

#         # Run the sweep
#         results, result_matrix = sweeper.sweep(
#             param_dict={"alpha3": alpha3_list, "alpha4": alpha4_list},
#             fixed_params={"method": "invcondition", "axes": "all"},
#             save_intermediate=False,
#         )
#         print(results)
#         print(result_matrix)


# if __name__ == "__main__":
#     unittest.main()
