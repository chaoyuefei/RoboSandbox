# sweep.py
import numpy as np
import pandas as pd
import itertools
import os
from tqdm import tqdm


class SweepResults:
    """
    Class to store and analyze results from parameter sweeps.
    """

    def __init__(self, sweep_data, variables, objective_values):
        """
        Initialize sweep results.

        :param sweep_data: Dictionary with variable names as keys and their values as lists
        :param variables: List of Variable objects involved in the sweep
        :param objective_values: List of objective function values for each parameter combination
        """
        self.sweep_data = sweep_data
        self.variables = variables
        self.objective_values = objective_values
        self.dataframe = self._create_dataframe()

    def _create_dataframe(self):
        """Create a pandas DataFrame from the sweep results."""
        data = {**self.sweep_data, "objective": self.objective_values}
        return pd.DataFrame(data)

    def get_optimal_point(self, minimize=True):
        """
        Get the parameter combination that results in the optimal objective value.

        :param minimize: If True, find minimum objective value; if False, find maximum
        :return: Dictionary with variable names and their optimal values
        """
        idx = (
            self.dataframe["objective"].idxmin()
            if minimize
            else self.dataframe["objective"].idxmax()
        )
        row = self.dataframe.iloc[idx]

        # Create a dictionary of variable names and their optimal values
        result = {}
        for var in self.variables:
            result[var.name] = row[var.name]
        result["objective"] = row["objective"]

        return result

    def save_to_csv(self, filepath):
        """Save the sweep results to a CSV file."""
        self.dataframe.to_csv(filepath, index=False)
        print(f"Results saved to {filepath}")

    def __str__(self):
        """String representation of sweep results."""
        return str(self.dataframe)


def solve_sweep(opti, variables_dict, save_path=None, **solve_kwargs):
    """
    Perform a parameter sweep by evaluating the objective function for different variable values.

    :param opti: The Opti instance
    :param variables_dict: Dictionary mapping Variables to lists of values or (start, stop, num_steps) tuples
    :param save_path: Optional path to save results to CSV file
    :param solve_kwargs: Additional arguments to pass to evaluate the objective
    :return: SweepResults object containing the results of the sweep
    """
    # Process input parameters
    processed_vars = {}
    var_objects = []

    for var, values in variables_dict.items():
        if not isinstance(var, opti.Variable):
            if isinstance(var, str):
                # Try to find the variable by name
                var = opti.variable_by_name(var)
            else:
                raise TypeError(f"Expected Variable object or string, got {type(var)}")

        var_objects.append(var)

        # Check if the values is a tuple representing a range
        if isinstance(values, tuple) and len(values) in [3, 4]:
            if len(values) == 3:
                start, stop, num = values
                step_type = "linear"
            else:
                start, stop, num, step_type = values

            if step_type == "linear":
                values = np.linspace(start, stop, num)
            elif step_type == "log":
                values = np.logspace(np.log10(start), np.log10(stop), num)
            else:
                raise ValueError(
                    f"Unknown step type: {step_type}. Use 'linear' or 'log'."
                )

        processed_vars[var.name] = values

    # Create all combinations of parameter values
    param_names = list(processed_vars.keys())
    param_values = list(processed_vars.values())
    combinations = list(itertools.product(*param_values))

    # Prepare data structures for results
    sweep_data = {name: [] for name in param_names}
    objective_values = []

    # Setup progress bar
    print(f"Running sweep with {len(combinations)} combinations...")

    # Perform the sweep
    for params in tqdm(combinations, desc="Sweeping parameters"):
        # Update the parameters for this iteration
        for i, var_name in enumerate(param_names):
            sweep_data[var_name].append(params[i])

            # Set the initial guess for the variable to the current sweep value
            var = opti.variable_by_name(var_name)
            var.init_guess = params[i]

        # Evaluate the objective function
        try:
            # If we're using a set objective function for optimization
            if opti.objective is not None:
                # Solve the optimization problem with updated initial guesses
                solution = opti.solve(**solve_kwargs)

                # Use the provided sweep objective if available, otherwise use the optimization objective
                if (
                    hasattr(opti, "sweep_objective")
                    and opti.sweep_objective is not None
                ):
                    if callable(opti.sweep_objective):
                        # If it's a callable function, call it with the solution
                        obj_value = opti.sweep_objective(solution)
                    else:
                        # Otherwise, treat it as an Expression and evaluate it
                        x = [solution(var) for var in opti.variables]
                        obj_value = opti.sweep_objective.evaluate(x, opti.parameters)
                else:
                    # Use the optimization result
                    obj_value = solution.result.fun
            else:
                # If no optimization objective, evaluate the sweep objective directly
                # This is for direct evaluation without optimization
                if (
                    hasattr(opti, "sweep_objective")
                    and opti.sweep_objective is not None
                ):
                    if callable(opti.sweep_objective):
                        # Create a dictionary of variable values for this iteration
                        var_values = {
                            var.name: params[i] for i, var in enumerate(var_objects)
                        }
                        obj_value = opti.sweep_objective(**var_values)
                    else:
                        # Evaluate the expression with the current parameter values
                        var_values = [0] * len(opti.variables)
                        for i, name in enumerate(param_names):
                            var = opti.variable_by_name(name)
                            var_values[var.index] = params[i]
                        obj_value = opti.sweep_objective.evaluate(
                            var_values, opti.parameters
                        )
                else:
                    raise ValueError(
                        "No objective function or sweep objective provided"
                    )

            objective_values.append(obj_value)

        except Exception as e:
            print(f"Error during sweep at {dict(zip(param_names, params))}: {str(e)}")
            objective_values.append(np.nan)

    # Create results object
    results = SweepResults(sweep_data, var_objects, objective_values)

    # Save results if requested
    if save_path:
        results.save_to_csv(save_path)

    return results
