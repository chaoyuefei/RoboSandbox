import numpy as np
from tqdm import tqdm
import itertools
from typing import Dict, List, Callable, Any, Union, Tuple


class ParameterSweeper:
    """
    A class for sweeping across parameter spaces and evaluating objective functions.
    """

    def __init__(self, objective_function: Callable):
        """
        Initialize the sweeper with an objective function to evaluate.

        Args:
            objective_function: Function that takes parameters and returns a value
            save_path: Path to save results (optional)
        """
        self.objective_function = objective_function
        # self.save_path = save_path
        self.results = None
        self.result_matrix = None

    def sweep(
        self,
        param_dict: Dict[str, List[Any]],
        fixed_params: Dict[str, Any] = None,
        display_progress: bool = True,
        save_intermediate: bool = False,
        intermediate_save_interval: int = 10,
        save_path: str = None,
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Sweep across parameter space and evaluate objective function.

        Args:
            param_dict: Dictionary mapping parameter names to lists of values
            fixed_params: Dictionary of fixed parameters to pass to objective function
            display_progress: Whether to display progress bars
            save_intermediate: Whether to save intermediate results
            intermediate_save_interval: How often to save intermediate results

        Returns:
            Tuple of (results array, result matrix)
        """
        if fixed_params is None:
            fixed_params = {}

        # Get parameter names and values
        param_names = list(param_dict.keys())
        param_values = list(param_dict.values())

        # Create result matrix of appropriate dimensionality
        matrix_shape = [len(values) for values in param_values]
        self.result_matrix = np.zeros(matrix_shape)

        # Create results list to store all parameter combinations and results
        results = []

        # Total iterations for progress tracking
        total_iterations = np.prod(matrix_shape)

        # Set up nested progress bars if requested
        if display_progress:
            outer_iter = tqdm(
                enumerate(param_values[0]),
                total=len(param_values[0]),
                desc=f"{param_names[0]} progress",
                unit="iter",
            )
        else:
            outer_iter = enumerate(param_values[0])

        # Counter for intermediate saves
        eval_count = 0

        # Iterate through all parameter combinations
        for i, val_0 in outer_iter:
            # Create nested loops for remaining parameters
            if len(param_names) > 1:
                if display_progress:
                    inner_iter = tqdm(
                        enumerate(param_values[1]),
                        total=len(param_values[1]),
                        desc=f"{param_names[1]} progress ({param_names[0]}={val_0})",
                        unit="iter",
                        leave=False,
                    )
                else:
                    inner_iter = enumerate(param_values[1])

                for j, val_1 in inner_iter:
                    # Handle deeper nesting if needed
                    if len(param_names) > 2:
                        remaining_params = self._evaluate_deeper_params(
                            param_names[2:],
                            param_values[2:],
                            [i, j],
                            [val_0, val_1],
                            fixed_params,
                            results,
                        )
                    else:
                        # Create parameter dictionary for this iteration
                        params = {
                            param_names[0]: val_0,
                            param_names[1]: val_1,
                            **fixed_params,
                        }

                        # Evaluate objective function
                        result = self.objective_function(**params)

                        # Store results
                        param_combination = [val_0, val_1]
                        results.append(param_combination + [result])
                        self.result_matrix[i, j] = result

                        # Increment counter and save if needed
                        eval_count += 1
                        if (
                            save_intermediate
                            and eval_count % intermediate_save_interval == 0
                        ):
                            self._save_results(results, self.result_matrix)
            else:
                # Single parameter case
                params = {param_names[0]: val_0, **fixed_params}

                # Evaluate objective function
                result = self.objective_function(**params)

                # Store results
                results.append([val_0, result])
                self.result_matrix[i] = result

                # Increment counter and save if needed
                eval_count += 1
                if save_intermediate and eval_count % intermediate_save_interval == 0:
                    self._save_results(results, self.result_matrix)

        # Convert results to numpy array
        self.results = np.array(results)

        # Save final results if path is provided
        if save_path:
            self._save_results(self.results, self.result_matrix, save_path)

        return self.results, self.result_matrix.T

    def _evaluate_deeper_params(
        self, param_names, param_values, indices, current_vals, fixed_params, results
    ):
        """Helper method to handle more than 2 nested parameters"""
        # This is a recursive method to handle arbitrary parameter depth
        if len(param_names) == 0:
            # Base case - evaluate with all parameters set
            all_param_names = list(fixed_params.keys())
            for i, stored_name in enumerate(self.param_names):
                if i < len(current_vals):
                    all_param_names[stored_name] = current_vals[i]

            result = self.objective_function(**all_param_names)

            # Store in results and matrix
            results.append(current_vals + [result])
            self.result_matrix[tuple(indices)] = result
            return result

        # Recursive case - handle the next parameter
        next_param_name = param_names[0]
        next_param_values = param_values[0]

        for k, val in enumerate(next_param_values):
            new_indices = indices + [k]
            new_current_vals = current_vals + [val]
            self._evaluate_deeper_params(
                param_names[1:],
                param_values[1:],
                new_indices,
                new_current_vals,
                fixed_params,
                results,
            )

    def _save_results(self, results, result_matrix, save_path):
        """Save results to file"""
        if save_path:
            np.savez(save_path, results=results, result_matrix=result_matrix)
