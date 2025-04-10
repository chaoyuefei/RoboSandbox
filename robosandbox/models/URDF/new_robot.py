#!/usr/bin/env python

import numpy as np
from roboticstoolbox.robot.ERobot import ERobot, ERobot2
from spatialmath import SE3


class New(ERobot):
    def __init__(self):
        links, name, urdf_string, urdf_filepath = self.URDF_read(
            file_path="outfile.xml", tld="./"
        )

        super().__init__(
            links,
            name=name,
            manufacturer="Chaoyue",
            # gripper_links=links[9],
            urdf_string=urdf_string,
            urdf_filepath=urdf_filepath,
        )

        # self.qr = np.array([0.7, -1, 0, -2.2, 0, np.pi / 4])
        self.qz = np.zeros(4)

        # self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)


if __name__ == "__main__":  # pragma nocover
    r = New()

    r.qz
    print(r)
    # r.plot(q=[0.2, -2, -0.3, 0.3, 0.4, 0.5], backend="swift", block=True)
    # r.plot(q=r.qz, backend="swift", block=True)
    print(r.fkine(r.qz))
    print(r.links[2])
    r.plot(q=[0, 0, 0, 0], backend="swift", block=True)
