from matplotlib.patches import Shadow
from typing import Union
import pandas as pd


class WorkSpace:
    def __init__(self):
        columns = ["x", "y", "z"]
        self.metrics = ["yoshikawa", "invcondition", "asada"]
        columns = columns + self.metrics
        self.df = pd.DataFrame(columns=columns)
        print(self.df)

    def add_samples(self, points, metric_values, metric: Union[str, None] = None):
        """
        Add samples to the workspace DataFrame.
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
