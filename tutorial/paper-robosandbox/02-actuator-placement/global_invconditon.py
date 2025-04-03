import numpy as np
from obj import obj
from plot_utils import plot_global_index_results
from robosandbox.optimization.sweeper import ParameterSweeper

np.random.seed(42)
# Create parameter sweeper
sweeper = ParameterSweeper(objective_function=obj)

# Define parameter ranges
step = 15
alpha1_list = np.deg2rad(np.arange(0, 181, step))
alpha2_list = np.deg2rad(np.arange(0, 181, step))

# Define method
method = "invcondition"

# Define lists for iterations
normalize_options = [True, False]
axes_options = ["trans", "all"]

# Loop through all combinations
for isNormalized in normalize_options:
    for axes in axes_options:
        # Create filename
        filename = f"data/two_alpha/{method}_{axes}_normalized_{isNormalized}.npz"

        isRun = True  # Set to False if you want to load saved data

        # Run the sweep or load data
        if not isRun:
            data = np.load(filename)
            results = data["results"]
            result_matrix = data["result_matrix"]
        else:
            results, result_matrix = sweeper.sweep(
                param_dict={"alpha1": alpha1_list, "alpha2": alpha1_list},
                fixed_params={
                    "method": method,
                    "axes": axes,
                    "is_normalized": isNormalized,
                },
                save_intermediate=False,
                save_path=filename,
            )

        # Round the results based on accepted precision
        results = np.round(results, 3)
        result_matrix = np.round(result_matrix, 3)

        # Plot the results
        plot_global_index_results(
            alpha_list_deg1=alpha1_list * 180 / np.pi,
            alpha_list_deg2=alpha2_list * 180 / np.pi,
            res_mat=result_matrix,
            plot_type="heatmap",
            method=method,
            axes=axes,
            isSave=True,
            isNormalized=isNormalized,
            step=step,
        )

        plot_global_index_results(
            alpha_list_deg1=alpha1_list * 180 / np.pi,
            alpha_list_deg2=alpha2_list * 180 / np.pi,
            res_mat=result_matrix,
            plot_type="surface",
            method=method,
            axes=axes,
            isSave=True,
            isNormalized=isNormalized,
            step=step,
        )

        print(f"Completed: method={method}, axes={axes}, isNormalized={isNormalized}")
