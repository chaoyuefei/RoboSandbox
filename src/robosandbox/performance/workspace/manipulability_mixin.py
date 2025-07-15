import numpy as np


class ManipulabilityMixin:
    def calc_manipulability(self, joint_points, method="yoshikawa", axes="all"):
        """
        Calculate the manipulability of the robot for given joint points.
        :param joint_points: list of joint points.
        :param method: str, the method used for calculating manipulability values.
        :param axes: str, the axes to calculate the manipulability.
        :return: values: np.array, the manipulability values.
        """
        return np.array(
            [
                self.robot.manipulability(point, method=method, axes=axes)
                for point in joint_points
            ]
        )
