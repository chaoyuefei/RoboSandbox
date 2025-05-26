import numpy as np
import pandas as pd
from typing import Callable, Optional, Union
from .indice_manager import IndiceManager


class WorkSpace:
    """
    Unified WorkSpace class for robotic workspace analysis.
    """

    def __init__(self, robot=None):
        self.robot = robot
        self.df = pd.DataFrame(columns=["x", "y", "z"])
        self.indice_manager = IndiceManager()

    def add_indice(self, method: str, function: Callable, *args, description: str = "", **kwargs):
        """
        Add a custom global indice function to the registry.

        :param method: str, the name of the custom indice.
        :param function: callable, a function that computes the indice.
        :param args: additional positional arguments for the function.
        :param description: str, a description of what the indice measures.
        :param kwargs: additional keyword arguments for the function.
        """
        self.indice_manager.add_indice(method, function, *args, description=description, **kwargs)

    def indice(self, method: str, *args, **kwargs) -> float:
        """
        Compute the global indice for the given method.

        :param method: str, the name of the metric or custom indice.
        :param joint_points: optional, joint points for manipulability calculations.
        :param args: additional positional arguments for the computation.
        :param kwargs: additional keyword arguments for the computation.
        :return: float, the computed global indice.
        """
        if method in self.indice_manager.list_indices():
            function, _, _, _ = self.indice_manager.get_indice(method)
            return function(self, *args, **kwargs)
        else:
            raise ValueError(f"Unknown method: {method}")

    def list_indice(self) -> list:
        """
        List all available indices.

        :return: list of str, the names of all registered indices.
        """
        return self.indice_manager.list_indices()

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
        # Filter out empty or all-NA entries before concatenation
        filtered_df = self.df.dropna(how="all", axis=1)  # Drop columns that are all NA
        filtered_points_df = points_df.dropna(how="all", axis=1)  # Same for points_df

        # Then concatenate the filtered DataFrames
        self.df = pd.concat(
            [filtered_df, filtered_points_df], axis=0, ignore_index=True
        )
