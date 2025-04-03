import numpy as np
from obj import obj
from plot_utils import plot_global_index_results
from robosandbox.optimization.sweeper import ParameterSweeper

np.random.seed(42)
# Create parameter sweeper
sweeper = ParameterSweeper(objective_function=obj)

# Define parameter ranges
step = 15
alpha3_list = np.deg2rad(np.arange(0, 181, step))
alpha4_list = np.deg2rad(np.arange(0, 181, step))

# Define the method and axes for the sweep
method = "invcondition"
axes = "trans"
isNormalized = False
isRun = True
filename = f"data/two_alpha/{method}_{axes}_normalized_{isNormalized}.npz"

# Run the sweep
if not isRun:
    data = np.load(filename)
    results = data["results"]
    result_matrix = data["result_matrix"]
else:
    results, result_matrix = sweeper.sweep(
        param_dict={"alpha3": alpha3_list, "alpha4": alpha4_list},
        fixed_params={"method": method, "axes": axes, "is_normalized": False},
        save_intermediate=False,
        save_path=filename,
    )

# round the results based on accepted precision
results = np.round(results, 3)
result_matrix = np.round(result_matrix, 3)

# Plot the results
plot_global_index_results(
    alpha_list_deg3=alpha3_list * 180 / np.pi,
    alpha_list_deg4=alpha4_list * 180 / np.pi,
    res_mat=result_matrix,
    plot_type="heatmap",
    method=method,
    axes=axes,
    isSave=True,
    isNormalized=isNormalized,
    step=step,
)

plot_global_index_results(
    alpha_list_deg3=alpha3_list * 180 / np.pi,
    alpha_list_deg4=alpha4_list * 180 / np.pi,
    res_mat=result_matrix,
    plot_type="surface",
    method=method,
    axes=axes,
    isSave=True,
    isNormalized=isNormalized,
    step=step,
)
