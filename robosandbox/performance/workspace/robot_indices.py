import numpy as np


def yoshikawa(workspace, joint_points, axes="all") -> np.ndarray:
    """
    Calculate the Yoshikawa manipulability index, one of the standard robot performance metrics.

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
    Calculate the inverse condition number index, a performance metric for robot dexterity.

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
    Calculate the Asada index, a performance metric based on minimum singular value.

    :param workspace: The workspace instance providing access to the robot.
    :param joint_points: List of joint configurations to evaluate.
    :param axes: Which axes to consider ('all', 'trans', 'rot').
    :return: The average Asada index.
    """
    return _calculate_manipulability(workspace, joint_points, method="asada", axes=axes)


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


# Mapping of string identifiers to index calculation method functions
METHOD_MAP = {"yoshikawa": yoshikawa, "invcondition": invcondition, "asada": asada}
