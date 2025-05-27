import robosandbox as rsb


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
        n = robot.dofs
        if det_H > 0:
            order_independent_manip = det_H ** (1 / n)
        else:
            order_independent_manip = 0

        results.append(order_independent_manip)

    return np.array(results)


import numpy as np

# Create robot model
# robot = rsb.models.DH.Generic.GenericSeven()
robot = rsb.models.DH.Panda()
ws = rsb.performance.workspace.WorkSpace(robot)

# Register the new manipulability index
ws.add_indice(
    method="order_independent_manipulability",
    function=order_independent_manipulability,
    description="Order-independent manipulability index (nth root of determinant)",
)

# Test the new index
print("Available indices:", ws.list_indice())

# Generate some joint configurations for testing
qlist = ws.generate_joints_samples(100)

# Calculate the order-independent manipulability index
result = ws.local_indice("order_independent_manipulability", joint_points=qlist)
print(f"Order-independent manipulability values for {len(result)} configurations:")
print(f"  Min: {np.min(result):.4f}")
print(f"  Max: {np.max(result):.4f}")
print(f"  Mean: {np.mean(result):.4f}")

# Compare with standard Yoshikawa index
yoshi_result = ws.local_indice("yoshikawa", joint_points=qlist)
print(f"\nStandard Yoshikawa values for {len(yoshi_result)} configurations:")
print(f"  Min: {np.min(yoshi_result):.4f}")
print(f"  Max: {np.max(yoshi_result):.4f}")
print(f"  Mean: {np.mean(yoshi_result):.4f}")

# Calculate the global indices
print("\nCalculating global indices (this may take a moment)...")
global_oim = ws.global_indice(
    initial_samples=500,  # Using fewer samples for demonstration
    method="order_independent_manipulability",
    max_samples=1000,
)
print(f"Global order-independent manipulability: {global_oim:.4f}")

global_yoshi = ws.global_indice(
    initial_samples=500,  # Using fewer samples for demonstration
    method="yoshikawa",
    max_samples=1000,
)
print(f"Global Yoshikawa manipulability: {global_yoshi:.4f}")
