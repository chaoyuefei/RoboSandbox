import numpy as np
from scipy.optimize import minimize

class Variable:
    _count = 0  # Class variable to assign unique IDs to variables

    def __init__(self, init_guess=0, name=None, bounds=(None, None)):
        """
        Initialize a decision variable.

        :param init_guess: Initial guess for the variable.
        :param name: Optional name for the variable.
        :param bounds: Bounds for the variable as a tuple (min, max).
        """
        self.init_guess = init_guess
        self.name = name if name else f"var_{Variable._count}"
        Variable._count += 1
        self.bounds = bounds
        self.index = None  # To be set by the Opti environment

    # Operator Overloading for Expression Building
    def __add__(self, other):
        return Expression('+', self, other)

    def __radd__(self, other):
        return Expression('+', other, self)

    def __sub__(self, other):
        return Expression('-', self, other)

    def __rsub__(self, other):
        return Expression('-', other, self)

    def __mul__(self, other):
        return Expression('*', self, other)

    def __rmul__(self, other):
        return Expression('*', other, self)

    def __truediv__(self, other):
        return Expression('/', self, other)

    def __rtruediv__(self, other):
        return Expression('/', other, self)

    def __pow__(self, power):
        return Expression('**', self, power)

    def __rpow__(self, base):
        return Expression('**', base, self)

    def __gt__(self, other):
        return Constraint('ineq', Expression('-', self, other))

    def __lt__(self, other):
        return Constraint('ineq', Expression('-', other, self))

    def __ge__(self, other):
        return Constraint('ineq', Expression('-', self, other))

    def __le__(self, other):
        return Constraint('ineq', Expression('-', other, self))

    def __eq__(self, other):
        return Constraint('eq', Expression('-', self, other))

class Expression:
    """
    Represents a mathematical expression built from Variables and constants.
    """
    def __init__(self, operator, left, right=None):
        self.operator = operator
        self.left = left
        self.right = right  # Can be None for unary operations

    def evaluate(self, var_values, params):
        """
        Recursively evaluate the expression given variable values and parameters.
        """
        # Evaluate left operand
        if isinstance(self.left, Variable):
            left_val = var_values[self.left.index]
        elif isinstance(self.left, Expression):
            left_val = self.left.evaluate(var_values, params)
        else:  # constant
            left_val = self.left

        # Evaluate right operand if present
        if self.right is not None:
            if isinstance(self.right, Variable):
                right_val = var_values[self.right.index]
            elif isinstance(self.right, Expression):
                right_val = self.right.evaluate(var_values, params)
            else:  # constant
                right_val = self.right

        # Perform the operation
        if self.operator == '+':
            return left_val + right_val
        elif self.operator == '-':
            return left_val - right_val
        elif self.operator == '*':
            return left_val * right_val
        elif self.operator == '/':
            return left_val / right_val
        elif self.operator == '**':
            return left_val ** right_val
        else:
            raise ValueError(f"Unsupported operator: {self.operator}")

    def to_callable(self, opti_env):
        """
        Convert the expression into a callable function that takes a variable vector.
        """
        def func(x):
            return self.evaluate(x, opti_env.parameters)
        return func

    # Operator Overloading Methods
    def __add__(self, other):
        return Expression('+', self, other)

    def __radd__(self, other):
        return Expression('+', other, self)

    def __sub__(self, other):
        return Expression('-', self, other)

    def __rsub__(self, other):
        return Expression('-', other, self)

    def __mul__(self, other):
        return Expression('*', self, other)

    def __rmul__(self, other):
        return Expression('*', other, self)

    def __truediv__(self, other):
        return Expression('/', self, other)

    def __rtruediv__(self, other):
        return Expression('/', other, self)

    def __pow__(self, power):
        return Expression('**', self, power)

    def __rpow__(self, base):
        return Expression('**', base, self)

class ExternalFunctionExpression(Expression):
    """
    Represents an external function as an expression in the optimization problem.
    """
    def __init__(self, func, variables):
        """
        Initialize with a callable function and the variables it depends on.

        :param func: A callable that takes inputs corresponding to the variables.
        :param variables: A list of Variable instances that the function depends on.
        """
        self.func = func
        self.variables = variables

    def evaluate(self, var_values, params):
        """
        Evaluate the external function with current variable values.

        :param var_values: List of variable values.
        :param params: Additional parameters (unused here).
        :return: The scalar result of the external function.
        """
        # Extract the current values of the involved variables
        current_values = [var_values[var.index] for var in self.variables]
        return self.func(*current_values)

class Constraint:
    """
    Represents a constraint in the optimization problem.
    """
    def __init__(self, type_, expression):
        """
        :param type_: 'eq' for equality, 'ineq' for inequality.
        :param expression: An Expression object representing the constraint.
        """
        assert type_ in ['eq', 'ineq'], "Constraint type must be 'eq' or 'ineq'."
        self.type = type_
        self.expression = expression

    def to_callable(self, opti_env):
        """
        Convert the constraint into a callable function for scipy.optimize.
        """
        def func(x):
            return self.expression.evaluate(x, opti_env.parameters)
        return {'type': self.type, 'fun': func}

class Solution:
    """
    Represents the solution to the optimization problem.
    """
    def __init__(self, result, variables):
        self.result = result
        self.variables = variables

    def __call__(self, var):
        if var.index >= len(self.result.x):
            raise IndexError("Variable index out of range.")
        return self.result.x[var.index]

    def success(self):
        return self.result.success

    def message(self):
        return self.result.message

class Opti:
    def __init__(self):
        """
        Initialize the optimization environment.
        """
        self.variables = []
        self.constraints = []
        self.objective = None
        self.objective_sense = 'min'  # 'min' or 'max'
        self.parameters = {}  # For additional parameters if needed

    def variable(self, init_guess=None, name=None, bounds=(None, None)):
        """
        Create and add a new variable to the environment.

        :param init_guess: Initial guess for the variable.
        :param name: Optional name for the variable.
        :param bounds: Bounds for the variable as a tuple (min, max).
        :return: The created Variable instance.
        """
        var = Variable(init_guess=init_guess, name=name, bounds=bounds)
        var.index = len(self.variables)  # Assign index based on order
        self.variables.append(var)
        return var

    def subject_to(self, constraint):
        """
        Add a constraint to the optimization problem.

        :param constraint: A Constraint instance.
        """
        if isinstance(constraint, Constraint):
            self.constraints.append(constraint)
        else:
            raise TypeError("Constraint must be an instance of Constraint class.")

    def minimize(self, objective_expr):
        """
        Set the objective function for minimization.

        :param objective_expr: An Expression representing the objective.
        """
        self.objective = objective_expr
        self.objective_sense = 'min'

    def maximize(self, objective_expr):
        """
        Set the objective function for maximization.

        :param objective_expr: An Expression representing the objective.
        """
        self.objective = objective_expr
        self.objective_sense = 'max'

    def solve(self, method='SLSQP'):
        """
        Solve the optimization problem using scipy.optimize.minimize.

        :param method: Optimization method to use.
        :return: A Solution instance containing the results.
        """
        if self.objective is None:
            raise ValueError("Objective function is not set.")

        # Prepare initial guesses and bounds
        initial_guess = [var.init_guess for var in self.variables]
        bounds = [var.bounds for var in self.variables]

        # Define the objective function
        if self.objective_sense == 'min':
            obj_func = lambda x: self.objective.evaluate(x, self.parameters)
        elif self.objective_sense == 'max':
            # To maximize, minimize the negative
            obj_func = lambda x: -self.objective.evaluate(x, self.parameters)
        else:
            raise ValueError("Objective sense must be 'min' or 'max'.")

        # Define constraints
        scipy_constraints = []
        for constr in self.constraints:
            scipy_constraints.append(constr.to_callable(self))

        # Perform optimization
        result = minimize(
            obj_func,
            initial_guess,
            method=method,
            bounds=bounds,
            constraints=scipy_constraints,
            options={'maxiter': 1000, 'disp': True}  # Set disp=False to control output
        )

        # If maximization, adjust the objective value
        if self.objective_sense == 'max' and result.success:
            result.fun = -result.fun

        return Solution(result, self.variables)
