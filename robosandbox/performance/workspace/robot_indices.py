import numpy as np


def yoshikawa(workspace, joint_points, axes="all") -> np.ndarray:
    """
    Yoshikawa index (determinant of Jacobian) - measures manipulability

    :param workspace: The workspace instance providing access to the robot.
    :param joint_points: List of joint configurations to evaluate.
    :param axes: Which axes to consider ('all', 'trans', 'rot').
    :return: The average Yoshikawa manipulability index.
    """
    return _calculate_manipulability(
        workspace, joint_points, method="yoshikawa", axes=axes
    )


def invcondition(workspace, joint_points, axes="all") -> np.ndarray:
    """
    Inverse condition number of the Jacobian - measures dexterity

    :param workspace: The workspace instance providing access to the robot.
    :param joint_points: List of joint configurations to evaluate.
    :param axes: Which axes to consider ('all', 'trans', 'rot').
    :return: The average inverse condition number index.
    """
    return _calculate_manipulability(
        workspace, joint_points, method="invcondition", axes=axes
    )


def asada(workspace, joint_points, axes="all") -> np.ndarray:
    """
    Asada index (minimum singular value) - measures worst-case performance

    :param workspace: The workspace instance providing access to the robot.
    :param joint_points: List of joint configurations to evaluate.
    :param axes: Which axes to consider ('all', 'trans', 'rot').
    :return: The average Asada index.
    """
    return _calculate_manipulability(workspace, joint_points, method="asada", axes=axes)


def order_independent_manipulability(
    workspace, joint_points, method="order_independent_manipulability", axes="all"
):
    """
    \sqrt[n]{(\operatorname{det}(\mathbf{H}(\mathbf{q}))}
    Calculate the order-independent manipulability index for a robot.
    Reference:
    Kim, J.-O., & Khosla, P. K. (1991). Dexterity measures for design and control of manipulators. IEEE/RJS International Conference on Intelligent RObots and Systems (IROS), 758–763. https://doi.org/10.1109/IROS.1991.174572


    :param workspace: The workspace instance providing access to the robot.
    :param joint_points: List of joint configurations to evaluate.
    :param method: The method name (for compatibility with the indice registry).
    :param axes: Which axes to consider ('all', 'trans', 'rot').
    :return: The order-independent manipulability indices for each configuration.
    """
    results = []

    for point in joint_points:
        if axes == "trans":
            J = workspace.robot.jacob0(point)[:3, :]
        if axes == "rot":
            J = workspace.robot.jacob0(point)[3:, :]
        if axes == "all":
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


def _calculate_manipulability(
    workspace, joint_points, method, axes="all"
) -> np.ndarray:
    """
    Base method to calculate any robot performance index. Powered by robotics toolbox python.

    :param workspace: The workspace instance providing access to the robot.
    :param joint_points: List of joint configurations to evaluate.
    :param method: The index method to use ('yoshikawa', 'invcondition', 'asada').
    :param axes: Which axes to consider ('all', 'trans', 'rot').
    :return: The list of index value.
    """
    if workspace.robot is None:
        raise ValueError("Robot is not set in the workspace")

    # Calculate manipulability for each joint configuration
    manipulability_values = np.array(
        [
            workspace.robot.manipulability(point, method=method, axes=axes)
            for point in joint_points
        ]
    )

    # Return the average manipulability
    return manipulability_values


# Dynamic mapping of string identifiers to index calculation method functions
# This is automatically populated from all non-private functions in this module
METHOD_MAP = {
    name: obj
    for name, obj in globals().items()
    if callable(obj)
    and not name.startswith("_")
    and hasattr(obj, "__module__")
    and obj.__module__ == __name__
}
