# %%
import robosandbox as rsb
import numpy as np
import plotly.graph_objects as go


# %%
def order_independent_manipulability(
    workspace, joint_points, method="order_independent_manipulability", axes="all"
):
    """
    \sqrt[n]{(\operatorname{det}(\mathbf{H}(\mathbf{q}))}
    Calculate the order-independent manipulability index for a robot.

    :param workspace: The workspace instance providing access to the robot.
    :param joint_points: List of joint configurations to evaluate.
    :param method: The method name (for compatibility with the indice registry).
    :param axes: Which axes to consider ('all', 'trans', 'rot').
    :return: The order-independent manipulability indices for each configuration.
    """
    results = []

    for point in joint_points:
        J = workspace.robot.jacob0(point)
        H = J @ J.T

        # Get the determinant of the manipulability matrix
        det_H = np.linalg.det(H)

        # Calculate the nth root of the determinant (n is the matrix dimension)
        n = workspace.robot.dofs
        if det_H > 0:
            order_independent_manip = det_H ** (1 / n)
        else:
            order_independent_manip = 0

        results.append(order_independent_manip)

    return np.array(results)


# %%
robot = rsb.models.DH.Panda()
ws = rsb.performance.workspace.WorkSpace(robot)

# Register the new manipulability index
ws.add_indice(
    method="order_independent_manipulability",
    function=order_independent_manipulability,
    description="Order-independent manipulability index (nth root of determinant)",
)

# Calculate the global indices
print("\nCalculating global indices (this may take a moment)...")
global_oim = ws.global_indice(method="order_independent_manipulability")
print(f"Global order-independent manipulability: {global_oim:.4f}")

# %%
fig = ws.plot(color="order_independent_manipulability", fig=go.Figure())
fig.show("png")

# %%
voxels = rsb.visualization.voxel_data.VoxelData(
    ws.df, method="order_independent_manipulability", voxel_size=0.1
)
fig = voxels.plot()
