#!/usr/bin/env python

import numpy as np
from roboticstoolbox.robot.Robot import Robot
from spatialmath import SE3


class Model(Robot):
    """
    Class that imports a URDF model from file.
    """

    def __init__(self, name, manufacturer, gripper_links, path):
        links, name, urdf_string, urdf_filepath = self.URDF_read(
            path,
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
#     r = Model()

#     r.qz

#     for link in r.grippers[0].links:
#         print(link)
