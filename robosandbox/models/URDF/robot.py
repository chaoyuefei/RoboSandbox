#!/usr/bin/env python

import numpy as np
from roboticstoolbox.robot.Robot import Robot
import swift


class CustomRobot(Robot):
    def __init__(self):
        links, name, urdf_string, urdf_filepath = self.URDF_read(
            file_path="outfile.xml", tld="./"
        )

        super().__init__(
            links,
            name=name.upper(),
            manufacturer="Chaoyue",
            urdf_string=urdf_string,
            urdf_filepath=urdf_filepath,
        )

        self.qr = np.array([np.pi, 0, 0, 0, np.pi / 2, 0])
        self.qz = np.zeros(6)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)


if __name__ == "__main__":  # pragma nocover
    robot = CustomRobot()
    print(robot)
    # env = swift.Swift()
    # env.launch(realtime=True)
    # env.add(robot)
