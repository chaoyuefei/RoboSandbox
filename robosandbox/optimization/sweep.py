# sweep.py
import numpy as np

class SweepResults:
    """
    Class to store and analyze the results of a parameter sweep.
    """
    def __init__(self, sweep_var_names):
        """
        Initialize the sweep results object.
        
        :param sweep_var_names: List of variable names that were swept
        """
        self.sweep_var_names = sweep_var_names
        self.results = []
        self.df = None  # Will be converted to pandas DataFrame for analysis
        
    def add_result(self, result_dict):
        """
        Add a single result to the collection.
        
        :param result_dict: Dictionary containing variable values and objective
        """
        self.results.append(result_dict)
        
    def to_dataframe(self):
        """
        Convert results to a pandas DataFrame for easier analysis.
        
        :return: pandas DataFrame of results
        """
        try:
            import pandas as pd
            self.df = pd.DataFrame(self.results)
            return self.df
        except ImportError:
            print("pandas not installed. Install with: pip install pandas")
            return None
            
    def save(self, path):
        """
        Save results to a CSV file.
        
        :param path: Path to save the CSV file
        """
        df = self.to_dataframe()
        if df is not None:
            df.to_csv(path, index=False)
            print(f"Results saved to {path}")
        
    def get_best_result(self, minimize=True):
        """
        Get the best result from the sweep.
        
        :param minimize: Whether to minimize or maximize the objective
        :return: Dictionary containing the best result
        """
        if not self.results:
            return None
            
        df = self.to_dataframe()
        if df is None:
            # Manual search if pandas isn't available
            valid_results = [r for r in self.results if r['success'] and not np.isnan(r['objective'])]
            if not valid_results:
                return None
                
            if minimize:
                return min(valid_results, key=lambda x: x['objective'])
            else:
                return max(valid_results, key=lambda x: x['objective'])
        else:
            # Use pandas for more efficient filtering and selection
            valid_df = df[df['success'] & ~df['objective'].isna()]
            if valid_df.empty:
                return None
                
            if minimize:
                idx = valid_df['objective'].idxmin()
            else:
                idx = valid_df['objective'].idxmax()
                
            return valid_df.loc[idx].to_dict()
            
    def plot(self, x_var, y_var='objective', groupby=None, **kwargs):
        """
        Plot sweep results.
        
        :param x_var: Variable name for x-axis
        :param y_var: Variable name for y-axis (default: 'objective')
        :param groupby: Optional variable name to group by
        :param kwargs: Additional arguments to pass to plotting function
        :return: matplotlib Figure and Axes objects
        """
        try:
            import matplotlib.pyplot as plt
            df = self.to_dataframe()
            
            if df is None:
                return None, None
                
            fig, ax = plt.subplots(figsize=(10, 6))
            
            if groupby:
                for name, group in df.groupby(groupby):
                    ax.plot(group[x_var], group[y_var], marker='o', linestyle='-', 
                            label=f"{groupby}={name}", **kwargs)
                ax.legend()
            else:
                ax.plot(df[x_var], df[y_var], marker='o', linestyle='-', **kwargs)
                
            ax.set_xlabel(x_var)
            ax.set_ylabel(y_var)
            ax.set_title(f"{y_var} vs {x_var}")
            ax.grid(True)
            
            return fig, ax
            
        except ImportError:
            print("matplotlib not installed. Install with: pip install matplotlib")
            return None, None

def solve_sweep(opti, variables_dict, save_path=None, **kwargs):
    """
    Perform a parameter sweep by solving the optimization problem for different variable values.
    
    :param opti: The Opti optimization object
    :param variables_dict: Dictionary mapping Variables to lists of values to sweep through
                          or tuples of (start, stop, num_steps) for linear spacing
    :param save_path: Optional path to save results to CSV file
    :param kwargs: Additional arguments to pass to solve() method
    :return: SweepResults object containing the results of the sweep
    """
    if not hasattr(opti, 'sweep_objective') or opti.sweep_objective is None:
        raise ValueError("Sweep objective not set. Call opti.sweep(obj) first.")
    
    # Process the variables_dict to create the grid of points to evaluate
    processed_vars = {}
    for var, values in variables_dict.items():
        if not hasattr(var, 'index'):  # Check if it's a Variable-like object
            raise TypeError(f"Keys in variables_dict must be Variable objects, got {type(var)}")
        
        if isinstance(values, tuple) and len(values) == 3:
            # Handle (start, stop, num_steps) format
            start, stop, num = values
            processed_vars[var] = np.linspace(start, stop, num)
        elif isinstance(values, (list, np.ndarray)):
            # Handle direct list of values
            processed_vars[var] = np.array(values)
        else:
            raise ValueError(f"Values must be a list, array, or (start, stop, num) tuple, got {type(values)}")
    
    # Create grid of all combinations
    var_names = [var.name for var in processed_vars.keys()]
    var_values = list(processed_vars.values())
    
    # Initialize results storage
    results = SweepResults(var_names)
    
    # Store the original state of the optimization problem
    original_objective = opti.objective
    original_sense = opti.objective_sense
    original_constraints = opti.constraints.copy()
    
    # Iterate through all combinations of variable values
    total_iterations = np.prod([len(vals) for vals in var_values])
    print(f"Running sweep with {total_iterations} iterations...")
    
    # Get flat indices for iteration
    if var_values:  # Check if there are any values to sweep through
        flat_indices = np.ndindex(tuple(len(vals) for vals in var_values))
    else:
        flat_indices = []  # Empty list if no values to sweep
    
    for idx in flat_indices:
        # Create a dictionary of current sweep variable values
        current_values = {var: var_values[i][idx[i]] for i, var in enumerate(processed_vars.keys())}
        
        # Set fixed values for the sweep variables by adding equality constraints
        opti.constraints = original_constraints.copy()
        for var, val in current_values.items():
            opti.subject_to(var == val)
        
        # Set the objective function based on the sweep objective
        if opti.objective_sense == 'min':
            opti.minimize(opti.sweep_objective)
        else:
            opti.maximize(opti.sweep_objective)
            
        # Solve the optimization problem
        try:
            solution = opti.solve(**kwargs)
            success = solution.success()
            obj_value = opti.sweep_objective.evaluate([solution(var) for var in opti.variables], opti.parameters) if success else np.nan
        except Exception as e:
            success = False
            obj_value = np.nan
            print(f"Error in iteration {idx}: {str(e)}")
            
        # Extract all variable values
        var_vals = {var.name: (solution(var) if success else np.nan) for var in opti.variables}
        
        # Add the sweep variable values and result
        sweep_vals = {var.name: current_values[var] for var in processed_vars.keys()}
        result_dict = {**sweep_vals, **var_vals, 'objective': obj_value, 'success': success}
        
        # Store the results
        results.add_result(result_dict)
        
    # Restore the original state
    opti.objective = original_objective
    opti.objective_sense = original_sense
    opti.constraints = original_constraints
    
    # Save results if requested
    if save_path:
        results.save(save_path)
        
    return results
