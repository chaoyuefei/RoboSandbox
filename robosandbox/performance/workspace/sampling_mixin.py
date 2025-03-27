import numpy as np


class SamplingMixin:
    def generate_joints_samples(self, num_samples: int, qlim=None):
        """
        Generate random samples and add them to the workspace DataFrame.
        :param num_samples: int, the number of samples to generate.
        :return: qlist
        """
        qlist = []
        qlim = self.robot.qlim if qlim is None else qlim
        for _ in range(num_samples):
            point = np.random.uniform(low=qlim[0], high=qlim[1])
            qlist.append(point)
        return qlist

    def get_cartesian_points(self, joint_points):
        """
        Get the cartesian points from the joint points.
        :param joint_points: list of joint points.
        :return: cartesian_points: list of cartesian points. (x, y, z)
        """
        cartesian_points = []
        for point in joint_points:
            T = self.robot.fkine(point)
            cartesian_points.append(T.t)
        return cartesian_points
