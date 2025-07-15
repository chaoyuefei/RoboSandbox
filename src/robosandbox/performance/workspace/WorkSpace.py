import numpy as np
import pandas as pd
from typing import Callable, Optional, Union
from .indice_manager import IndiceManager
from robosandbox.visualization.plotly_WorkSpace import PlotlyWorkSpace


class WorkSpace(PlotlyWorkSpace):
    """
    Unified WorkSpace class for robotic workspace analysis.
    """

    def __init__(self, robot=None):
        self.robot = robot
        self.df = pd.DataFrame(columns=["x", "y", "z"])
        self.indice_manager = IndiceManager()
        PlotlyWorkSpace.__init__(self, df=self.df)

    def add_indice(
        self, method: str, function: Callable, *args, description: str = "", **kwargs
    ):
        """
        Add a custom global indice function to the registry.

        :param method: str, the name of the custom indice.
        :param function: callable, a function that computes the indice.
        :param args: additional positional arguments for the function.
        :param description: str, a description of what the indice measures.
        :param kwargs: additional keyword arguments for the function.
        """
        self.indice_manager.add_indice(
            method, function, *args, description=description, **kwargs
        )

    def local_indice(self, method: str, *args, **kwargs) -> float:
        """
        Compute the local indice for the given method.

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

    def _calc_global_indice(
        self,
        method: str = "yoshikawa",
        is_normalized: bool = False,
        *args,
        **kwargs,
    ) -> float:
        sum_of_metric = self.df[method].sum()
        max_of_metric = self.df[method].max()
        num_samples = len(self.df)

        # standard normalization
        if is_normalized:
            if max_of_metric == 0:
                G = sum_of_metric / num_samples
            else:
                G = sum_of_metric / (num_samples * max_of_metric)
            return G
        # if other normalization methods
        if is_normalized and normalization_method is not None:
            G = normalization_method(self.df[method], *args, **kwargs)
            return G

        if not is_normalized:
            G = sum_of_metric / num_samples
            return G

    def global_indice(
        self,
        initial_samples: int = 3000,
        batch_ratio: float = 0.1,
        error_tolerance_percentage: float = 1e-2,
        method: str = "yoshikawa",
        max_samples: int = 20000,
        is_normalized: bool = False,
        *args,
        **kwargs,
    ) -> float:
        """
        Compute the global indice for the robotic manipulator.

        :param method: str, the metric to use for calculation (default is "yoshikawa").
        :param is_normalized: bool, flag indicating whether to normalize the indice (default is False).
        :return: float, the computed global indice value.
        """
        qlist = self.generate_joints_samples(initial_samples)
        self.add_samples(
            points=self.get_cartesian_points(qlist),
            metric_values=self.local_indice(
                method, joint_points=qlist, *args, **kwargs
            ),
            metric=method,
        )
        current_G = self._calc_global_indice(
            method=method, is_normalized=is_normalized, *args, **kwargs
        )
        if current_G == 0:
            return 0.0

        prev_G = 0
        err_relative = np.abs(prev_G - current_G) / current_G
        iteration = 1
        # Iteratively refine the global indice until convergence.
        while err_relative > error_tolerance_percentage and len(self.df) < max_samples:
            num_samples = int(len(self.df) * batch_ratio)
            qlist = self.generate_joints_samples(num_samples)
            self.add_samples(
                points=self.get_cartesian_points(qlist),
                metric_values=self.local_indice(
                    method, joint_points=qlist, *args, **kwargs
                ),
                metric=method,
            )
            prev_G = current_G
            current_G = self._calc_global_indice(
                method=method, is_normalized=is_normalized, *args, **kwargs
            )
            err_relative = np.abs(prev_G - current_G) / current_G
            iteration += 1
        return current_G

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

    def reach(self, axes="all"):
        """
        return the workspace reach in axis x, y, z or all axis
        """
        x_range = [self.df["x"].min(), self.df["x"].max()]
        y_range = [self.df["y"].min(), self.df["y"].max()]
        z_range = [self.df["z"].min(), self.df["z"].max()]
        if axes == "x":
            return x_range
        elif axes == "y":
            return y_range
        elif axes == "z":
            return z_range
        elif axes == "all":
            return [x_range, y_range, z_range]

    def get_volume(self, origin=[0, 0, 0], method="sphere"):
        if method == "sphere":
            r = self.get_max_distance(origin)
            return (4 / 3) * np.pi * r**3
