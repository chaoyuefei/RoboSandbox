from typing import Union
import numpy as np
import pandas as pd
from robosandbox.visualization.plotly_WorkSpace import PlotlyWorkSpace


class WorkSpace(PlotlyWorkSpace):
    def __init__(self, robot=None):
        columns = ["x", "y", "z"]
        self.metrics = ["yoshikawa", "invcondition", "asada"]
        columns = columns + self.metrics
        self.df = pd.DataFrame(columns=columns)
        self.robot = robot
        super().__init__(df=self.df)

    def add_samples(self, points, metric_values=None, metric: Union[str, None] = None):
        """
        Add samples and theirs values to the workspace DataFrame.
        :param points: list of tuples, containing the x, y, z coordinates of the samples.
        :param metric_values: list of floats, containing the metric values of the samples.
        :param metric: str, the name of the metric.
        :return: self.df: DataFrame, the updated workspace DataFrame.
        """
        points_df = pd.DataFrame(points, columns=self.df.columns[:3])
        # Add the metric values to the new samples DataFrame
        points_df[metric] = metric_values
        # Concatenate the existing DataFrame with the new samples
        self.df = pd.concat([self.df, points_df], axis=0, ignore_index=True)

    def add_new_metric(self, metric: str):
        """
        Add a new metric to the workspace DataFrame.
        :param metric: str, the name of the metric.
        :return: self.df: DataFrame, the updated workspace DataFrame.
        """
        self.df[metric] = None
        self.metrics.append(metric)

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

    def get_max_distance(self, origin=[0, 0, 0]):
        """
        Calculate the maximum Euclidean distance of all points from the specified origin.

        Args:
            origin (list or array-like, optional): The origin point [x, y, z]. Defaults to [0, 0, 0].

        Returns:
            float: The maximum distance from the origin. Returns 0 if no points are present.
        """
        origin = np.array(origin)
        points = self.df[["x", "y", "z"]].to_numpy(dtype=float)
        if points.size == 0:
            return 0.0
        # Handle possible NaN values by ignoring them in distance calculation
        valid_points = points[~np.isnan(points).any(axis=1)]
        if valid_points.size == 0:
            return 0.0
        distances = np.sqrt(np.sum((valid_points - origin) ** 2, axis=1))
        max_distance = np.max(distances)
        return max_distance

    def get_volume(self, origin=[0, 0, 0], method="sphere"):
        if method == "sphere":
            r = self.get_max_distance(origin)
            return (4 / 3) * np.pi * r**3

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

    def calc_global_indice(
        self,
        method="yoshikawa",
        isNormalized=False,
    ):
        v = self.get_volume()
        S_max = self.df[method].max()
        S_sum = self.df[method].sum(skipna=True)
        if isNormalized:
            S_sum_div = S_sum / (len(self.df) * S_max)
            G = S_sum_div / v
        else:
            G = S_sum / len(self.df)
        return G

    def iter_calc_global_indice(
        self,
        initial_samples=3000,
        batch_ratio=0.1,
        error_tolerance_percentage=1e-2,
        method="yoshikawa",
        axes="all",
        max_samples=20000,
        is_normalized=False,
    ):
        """
        Computes the global indices for a given robotic manipulator.
        Args:
            initial_samples: The starting number of random joint samples.
            batch_ratio: How many additional samples to add in each iteration.
            error_tolerance_percentage: The error threshold for stopping the iterations.
            method: The method used for calculating manipulability values.
            axes: The axes to calculate the manipulability.
            max_samples: The maximum number of samples to use.
        Returns:
            G: np.array, the computed global indices after convergence.
        """
        qlist = self.generate_joints_samples(initial_samples)
        self.add_samples(
            points=self.get_cartesian_points(qlist),
            metric_values=self.calc_manipulability(qlist, method=method, axes=axes),
            metric=method,
        )
        prev_G = 0
        current_G = self.calc_global_indice(method=method, isNormalized=is_normalized)
        err_relative = np.abs(prev_G - current_G) / current_G
        iteration = 1
        while err_relative > error_tolerance_percentage and len(self.df) < max_samples:
            num_samples = int(len(self.df) * batch_ratio)
            qlist = self.generate_joints_samples(num_samples)
            self.add_samples(
                points=self.get_cartesian_points(qlist),
                metric_values=self.calc_manipulability(qlist, method=method, axes=axes),
                metric=method,
            )
            prev_G = current_G
            current_G = self.calc_global_indice(
                method=method, isNormalized=is_normalized
            )
            err_relative = np.abs(prev_G - current_G) / current_G
            iteration += 1
            # if len(self.df) % 10 == 0:
            #     print(f"Iteration: {iteration}")
            #     print(f"Current number of samples: {len(self.df)}")
            #     print(f"Current global indice: {current_G}")
            #     print(f"Current relative error: {err_relative}")

        # print("==> Iteration finished.")
        # print(f"Converged after {iteration} iterations.")
        # print(f"Final global indice: {current_G}")
        # print(f"Final number of samples: {len(self.df)}")
        # print(f"Final relative error: {err_relative}")
        return current_G
