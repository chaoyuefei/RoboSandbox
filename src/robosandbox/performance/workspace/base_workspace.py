import pandas as pd
from typing import Union
import numpy as np
import pandas as pd


class BaseWorkSpace:
    def __init__(self, robot=None):
        columns = ["x", "y", "z"]
        self.metrics = ["yoshikawa", "invcondition", "asada"]
        columns = columns + self.metrics
        self.df = pd.DataFrame(columns=columns)
        self.robot = robot

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

    def add_new_metric(self, metric: str):
        """
        Add a new metric to the workspace DataFrame.
        :param metric: str, the name of the metric.
        :return: self.df: DataFrame, the updated workspace DataFrame.
        """
        self.df[metric] = None
        self.metrics.append(metric)

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
