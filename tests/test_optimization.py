import unittest
import robosandbox as rsb


class TestRobotOptimization(unittest.TestCase):
    def test_opti(self):
        """
        Test the optimization functionality.
        """
        # Create optimization problem
        opti = rsb.optimization.opti_scipy.Opti()
        # Define variables with initial guesses and bounds
        x = opti.variable(init_guess=5, name="x")
        y = opti.variable(init_guess=0, name="y")

        # Define an objective function: f = x^2 + y^2
        f = x**2 + y**2
        opti.minimize(f)

        # Add constraints: x > 3 and y >= 2
        opti.subject_to(x > 3)
        opti.subject_to(y >= 2)
        opti.subject_to(x + y <= 7)

        # Solve the optimization problem
        sol = opti.solve()

        # Check the solution
        self.assertTrue(sol.success())
        self.assertAlmostEqual(sol(x), 3, places=2)
        self.assertAlmostEqual(sol(y), 2, places=2)
        self.assertAlmostEquals(sol.result.fun, 13, places=2)

    def test_opti_01(self):
        """
        Test the optimization functionality.
        """
        # Create optimization problem
        opti = rsb.optimization.opti_scipy.Opti()
        # Define variables with bounds
        x = opti.variable(name="x", bounds=(0, 5), init_guess=1)
        y = opti.variable(name="y", bounds=(0, 5), init_guess=1)

        # Define objective function
        obj = (x - 2) ** 2 + (y - 1) ** 2

        # Add constraint
        opti.subject_to(x + y >= 3)

        # Solve without sweep to verify
        opti.minimize(obj)
        sol = opti.solve()

        self.assertTrue(sol.success())
        self.assertAlmostEqual(sol(x), 2, places=2)
        self.assertAlmostEqual(sol(y), 1, places=2)
        self.assertAlmostEqual(sol.result.fun, 0, places=2)

    def test_opti_external_function(self):
        """
        Test the optimization functionality with an external function.
        """
        # Create optimization problem
        opti = rsb.optimization.opti_scipy.Opti()
        # Define variables with bounds
        x = opti.variable(name="x", bounds=(0, 5), init_guess=1)
        y = opti.variable(name="y", bounds=(0, 5), init_guess=1)

        # Define objective function
        # obj = (x - 2) ** 2 + (y - 1) ** 2
        def obj_func(x, y, a, b):
            return (x - 2) ** 2 + (y - 1) ** 2 + a + b

        # Add constraint
        opti.subject_to(x + y >= 3)

        obj = opti.external_func(
            func=lambda x_var, y_var: obj_func(x_var, y_var, 1, 1),
            variables=[x, y],
        )

        # Solve without sweep to verify
        opti.minimize(obj)
        sol = opti.solve()

        self.assertTrue(sol.success())
        self.assertAlmostEqual(sol(x), 2, places=2)
        self.assertAlmostEqual(sol(y), 1, places=2)
        self.assertAlmostEqual(sol.result.fun, 2, places=2)


if __name__ == "__main__":
    unittest.main()
