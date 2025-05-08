import numpy as np
from pymoo.problems.functional import FunctionalProblem


class DesignProblem(FunctionalProblem):
    def __init__(self, n_var, xl, xu, objs, constr_ieq, constr_eq):
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

        # Optional: Track best solution or other custom information
        if hasattr(self, "best_f") and len(f) == 1:
            if not hasattr(self, "best_f") or f[0] < self.best_f:
                self.best_f = f[0]
                self.best_x = x.copy()

        # Return the evaluation results
        return out


if __name__ == "__main__":
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
    X = np.random.rand(
        10, 3
    )  # Changed from (3, 10) to (10, 3) for 10 points with 3 variables each
    F, G = problem.evaluate(X)

    print(f"F: {F}\n")
    print(f"G: {G}\n")
    print(f"Number of evaluations: {problem.counter}")
