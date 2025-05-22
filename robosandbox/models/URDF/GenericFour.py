#!/usr/bin/env python

import numpy as np
from roboticstoolbox.robot.ERobot import ERobot

import robosandbox


class GenericFour(ERobot):
    def __init__(self):
        links, name, urdf_string, urdf_filepath = self.URDF_read(
            file_path="GenericFour.urdf", tld="rsb-data"
        )

        super().__init__(
            links,
            name=name,
            manufacturer="Chaoyue",
            urdf_string=urdf_string,
            urdf_filepath=urdf_filepath,
        )
        self.qlim = np.array(
            [[-np.pi, -np.pi, -np.pi, -np.pi], [np.pi, np.pi, np.pi, np.pi]]
        )

        self.qz = np.zeros(4)
        self.qr = np.array([0, -0.8, 0.8, 0.8])
        self.addconfiguration("qz", self.qz)
        self.addconfiguration("qr", self.qr)


if __name__ == "__main__":  # pragma nocover
    from roboticstoolbox import jtraj
    import swift

    robot = robosandbox.models.URDF.GenericFour.GenericFour()
    q0 = robot.qz
    qe = robot.qr
    qtraj = jtraj(q0, qe, 100)

    env = swift.Swift()  # instantiate 3D browser-based visualizer       # activate it
    env.launch(realtime=True)
    env.add(robot)  # add robot to the 3D scene
    dt = 0.05
    # env.start_recording("G4", 1 / dt, format="gif")
    for qk in qtraj.q:  # for each joint configuration on trajectory
        robot.q = qk  # update the robot state
        env.step()  # update visualization

    # env.stop_recording()
    # env.close()
