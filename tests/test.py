import numpy as np
import robosandbox as rsb
from robosandbox.performance.workspace.indice_manager import (
    IndiceManager,
    IndiceRegistry,
)
from robosandbox.performance.workspace.WorkSpace import WorkSpace
import roboticstoolbox as rtb


def main():
    # robot = rtb.models.Panda()
    robot = rsb.models.DH.Panda()
    workspace = WorkSpace(robot)
    num_samples = 10
    joint_points = workspace.generate_joints_samples(num_samples)
    print(f"Generated {num_samples} joint configurations")
    # calculate yoshikawa
    values = workspace.indice(method="yoshikawa", joint_points=joint_points, axes="all")
    print(f"Yoshikawa value: {values}")
    # compare with robot manipulability
    robot_values = np.array(
        [
            robot.manipulability(point, method="yoshikawa", axes="all")
            for point in joint_points
        ]
    )
    print(f"Robot Yoshikawa value: {robot_values}")


if __name__ == "__main__":
    main()
