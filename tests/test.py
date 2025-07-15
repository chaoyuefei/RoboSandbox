import numpy as np
import robosandbox as rsb
import robosandbox.models as rsb_models
from robosandbox.performance.workspace.indice_manager import (
    IndiceManager,
    IndiceRegistry,
)
from robosandbox.performance.workspace.WorkSpace import WorkSpace
import roboticstoolbox as rtb


def main():
    # robot = rtb.models.Panda()
    robot = rsb.models.DH.Panda.Panda()
    robot = rsb_models.DH.UR5.UR5()
    # robot = rsb.models.DH.Generic.GenericTwo()
    workspace = WorkSpace(robot)
    num_samples = 1
    joint_points = workspace.generate_joints_samples(num_samples)
    print(f"Robot.qlim: {robot.qlim.shape}")
    print(f"Joint points: {joint_points}")
    print(f"Generated {num_samples} joint configurations")
    # calculate yoshikawa
    values = workspace.local_indice(
        method="invcondition", joint_points=joint_points, axes="all"
    )
    print(f"Yoshikawa value: {values}")
    # compare with robot manipulability
    robot_values = np.array(
        [
            robot.manipulability(point, method="invcondition", axes="all")
            for point in joint_points
        ]
    )
    print(f"Robot Yoshikawa value: {robot_values}")

    # calculate global indices
    G = workspace.global_indice(method="invcondition", axes="all", is_normalized=False)
    print("Global Yoshikawa value:", G)


if __name__ == "__main__":
    main()
