#!/usr/bin/env python

import numpy as np
from roboticstoolbox.robot.ERobot import ERobot


class GenericFour(ERobot):
    def __init__(self):
        links, name, urdf_string, urdf_filepath = self.URDF_read(
            file_path="GenericFour.urdf", tld="./data/"
        )

        super().__init__(
            links,
            name=name,
            manufacturer="Chaoyue",
            urdf_string=urdf_string,
            urdf_filepath=urdf_filepath,
        )

        self.qz = np.zeros(4)
        self.addconfiguration("qz", self.qz)


if __name__ == "__main__":  # pragma nocover
    from roboticstoolbox import jtraj
    import swift

    robot = GenericFour()
    q0 = robot.qz
    qe = np.array([0.7, -1, 0, 1.2])
    qtraj = jtraj(q0, qe, 100)

    env = swift.Swift()  # instantiate 3D browser-based visualizer       # activate it
    env.launch(realtime=True)
    env.add(robot)  # add robot to the 3D scene
    for qk in qtraj.q:  # for each joint configuration on trajectory
        robot.q = qk  # update the robot state
        env.step()  # update visualization
