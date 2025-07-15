#!/usr/bin/env python

import numpy as np
from roboticstoolbox.robot.Robot import Robot
from spatialmath import SE3


class Model(Robot):
    """
    Class that imports a URDF model from file.
    file_path: str
        Path to the URDF file.
    tld: str
        Top-level directory for the URDF file, used for resolving relative paths.
    xacro_tld: str
        Top-level directory for XACRO files, used for resolving relative paths in XACRO files.
    name: str
        Name of the robot model.
    manufacturer: str
        Manufacturer of the robot model.
    gripper_links: list
        List of gripper links, if any. If not provided, defaults to an empty list.
    This class reads the URDF file, extracts the links, and initializes the robot model.
    """

    def __init__(
        self,
        file_path: str,
        tld: str = "",
        xacro_tld: str = "",
        name: str = "",
        manufacturer: str = "",
        gripper_links=None,
    ):
        links, name, urdf_string, urdf_filepath = self.URDF_read(
            file_path=file_path,
            tld=tld,
            xacro_tld=xacro_tld,
        )

        super().__init__(
            links,
            name=name,
            manufacturer=manufacturer,
            gripper_links=gripper_links,
            urdf_string=urdf_string,
            urdf_filepath=urdf_filepath,
        )

        # self.grippers[0].tool = SE3(0, 0, 0.1034)

        # self.qdlim = np.array(
        #     [2.1750, 2.1750, 2.1750, 2.1750, 2.6100, 2.6100, 2.6100, 3.0, 3.0]
        # )


# if __name__ == "__main__":  # pragma nocover
# SO101 = Model(
#     name="SO101",
#     file_path="so100.urdf",
#     tld="/Users/chaoyue/Documents/coding/RoboSandbox/robosandbox/models/URDF/data/SO100",
# )
# SO101.q = np.zeros(6)
# print(SO101)
# SO101.plot(q=SO101.q)
