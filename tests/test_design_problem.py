import unittest
import numpy as np
from robosandbox.optimization.problem import DesignProblem


class TestDesignProblem(unittest.TestCase):
    def setUp(self):
        self.objs = [lambda x: np.sum((x - 2) ** 2), lambda x: np.sum((x + 2) ** 2)]
        self.constr_ieq = [lambda x: np.sum((x - 1) ** 2)]
        self.n_var = 3
        self.xl = np.array([-10, -5, -10])
        self.xu = np.array([10, 5, 10])
        self.problem = DesignProblem(
            n_var=self.n_var,
            xl=self.xl,
            xu=self.xu,
            objs=self.objs,
            constr_ieq=self.constr_ieq,
            constr_eq=[],
        )

    def test_evaluate_objectives(self):
        # Test evaluation of objective functions with a known design point.
        X = np.array([[2, 2, 2]])
        results = {}
        self.problem._evaluate(X, results)
        # Expected results: For x = [2,2,2]
        # First objective: sum((x-2)**2) = 0, second objective: sum((x+2)**2) = 48
        expected_F = np.array([0, 48])
        np.testing.assert_array_almost_equal(results["F"], expected_F)

    def test_evaluation_counter(self):
        # Test that the evaluation counter increments properly.
        X = np.array([[2, 2, 2]])
        initial_counter = self.problem.counter
        results = {}
        self.problem._evaluate(X, results)
        self.assertEqual(self.problem.counter, initial_counter + 1)

    def test_constraints_evaluation(self):
        # Test evaluation of inequality constraints.
        X = np.array([[1, 1, 1]])
        results = {}
        self.problem._evaluate(X, results)
        # For x = [1,1,1], inequality constraint: sum((x-1)**2) = 0
        expected_G = np.array([0])
        np.testing.assert_array_almost_equal(results["G"], expected_G)


if __name__ == "__main__":
    unittest.main()
