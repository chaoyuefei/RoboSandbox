"""
Design Problem Module
======================

This module defines the `DesignProblem` class which is used for optimization
problems using a functional approach. The class inherits from `FunctionalProblem`
of the pymoo library and implements the evaluation of objective function(s) and constraint(s)
for optimization problems.

Example:
    Define a simple design problem with two objectives and one inequality constraint, then solve
    for a set of random design points.

    >>> import numpy as np
    >>> from robosandbox.optimization.problem import DesignProblem
    >>> objs = [lambda x: np.sum((x - 2) ** 2), lambda x: np.sum((x + 2) ** 2)]
    >>> constr_ieq = [lambda x: np.sum((x - 1) ** 2)]
    >>> n_var = 3
    >>> problem = DesignProblem(
    ...     n_var=n_var,
    ...     objs=objs,
    ...     constr_ieq=constr_ieq,
    ...     constr_eq=[],
    ...     xl=np.array([-10, -5, -10]),
    ...     xu=np.array([10, 5, 10]),
    ... )
    >>> X = np.random.rand(10, 3)
    >>> F, G = problem.evaluate(X)
    >>> print(F)
    >>> print(G)

"""

import numpy as np
from pymoo.problems.functional import FunctionalProblem


class DesignProblem(FunctionalProblem):
    """
    DesignProblem class for Optimization Problems.
    ==============================================

    This class extends the `FunctionalProblem` from pymoo to evaluate both multiple
    objective functions and constraints. It also maintains an evaluation counter and
    conditional tracking of the best solution for single objective problems.

    Attributes:
        counter (int): The evaluation counter that tracks the number of evaluations performed.
        best_f (float, optional): The best objective function value encountered (if applicable).
        best_x (np.ndarray, optional): The best design point corresponding to `best_f`.
    """

    def __init__(self, n_var, xl, xu, objs, constr_ieq, constr_eq):
        """
        Initialize the DesignProblem.

        Parameters
        ----------
        n_var : int
            The number of variables in the design problem.
        xl : np.ndarray
            The lower bounds for the variables.
        xu : np.ndarray
            The upper bounds for the variables.
        objs : list of callable
            A list of objective functions that take a design vector and return a scalar value.
        constr_ieq : list of callable
            A list of inequality constraint functions. Each function should return a value that
            is expected to be non-negative if the constraint is satisfied.
        constr_eq : list of callable
            A list of equality constraint functions. Each function should ideally return zero when
            the constraint is satisfied.
        """
        super().__init__(
            n_var=n_var,
            objs=objs,
            constr_ieq=constr_ieq,
            constr_eq=constr_eq,
            xl=xl,
            xu=xu,
        )
        self.counter = 0

    def _evaluate(self, x, out, *args, **kwargs):
        """
        Evaluate the design problem at given design points.

        The method computes the objective function(s) and constraint(s) for the provided design
        points and updates an evaluation counter. For problems with a single objective, the
        method maintains a record of the best design point found.

        Parameters
        ----------
        x : np.ndarray
            The input design points (each row is a design vector).
        out : dict
            A dictionary to store the evaluation results.
        args : tuple
            Additional positional arguments.
        kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        dict
            The dictionary `out` updated with keys:
                - "F": np.ndarray containing the evaluated objective function values.
                - "G": np.ndarray containing the evaluated inequality constraints (if provided).
                - "H": np.ndarray containing the evaluated equality constraints (if provided).
        """
        # Increment evaluation counter
        self.counter += 1

        # Evaluate objective functions
        f = []
        for obj in self.objs:
            f.append(obj(x))
        out["F"] = np.array(f)

        # Evaluate inequality constraints if they exist
        if self.constr_ieq:
            g = []
            for constr in self.constr_ieq:
                g.append(constr(x))
            out["G"] = np.array(g)

        # Evaluate equality constraints if they exist
        if self.constr_eq:
            h = []
            for constr in self.constr_eq:
                h.append(constr(x))
            out["H"] = np.array(h)

        # Optional: Track best solution or other custom information for single objective problems
        if hasattr(self, "best_f") and len(f) == 1:
            if not hasattr(self, "best_f") or f[0] < self.best_f:
                self.best_f = f[0]
                self.best_x = x.copy()

        # Return the evaluation results
        return out


if __name__ == "__main__":
    """
    Execute a test run of the DesignProblem.
    =========================================

    This block defines a sample optimization problem instance with two objectives and one inequality constraint.
    It generates 10 random design points and evaluates them using the created problem instance, printing the
    objective and constraint values along with the number of evaluations performed.
    """
    # Define objective functions
    objs = [lambda x: np.sum((x - 2) ** 2), lambda x: np.sum((x + 2) ** 2)]

    # Define inequality constraint
    constr_ieq = [lambda x: np.sum((x - 1) ** 2)]

    # Number of variables
    n_var = 3  # Changed to 3 based on the dimension of xl and xu vectors

    # Create the problem using DesignProblem instead of FunctionalProblem
    problem = DesignProblem(
        n_var=n_var,
        objs=objs,
        constr_ieq=constr_ieq,
        constr_eq=[],
        xl=np.array([-10, -5, -10]),
        xu=np.array([10, 5, 10]),
    )

    # Generate 10 random design points with 3 variables each
    X = np.random.rand(10, 3)  # 10 points with 3 variables each
    F, G = problem.evaluate(X)

    print(f"F: {F}\n")
    print(f"G: {G}\n")
    print(f"Number of evaluations: {problem.counter}")
