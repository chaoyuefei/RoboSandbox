import unittest
from robosandbox.models.DH.Generic.GenericFour import GenericFour
from robosandbox.performance.workspace import WorkSpace
import numpy as np


class TestVisualization(unittest.TestCase):
    def test_workspace_distribution(self):
        robot = GenericFour(alpha=[np.pi / 2, np.pi / 2, 0, 0])
        ws = WorkSpace(robot)
        G = ws.global_indice(
            initial_samples=3000,
            batch_ratio=0.1,
            error_tolerance_percentage=1e-2,
            method="yoshikawa",
            axes="trans",
            max_samples=50000,
            is_normalized=False,  # Use the slider value here
        )
        ws.plot_zero_approach(data_column="yoshikawa", color_scheme="greens")

    def test_workspace_plot(self):
        robot = GenericFour(alpha=[np.pi / 2, 0, 0, 0])
        ws = WorkSpace(robot)
        G = ws.global_indice(
            initial_samples=3000,
            batch_ratio=0.1,
            error_tolerance_percentage=1e-2,
            method="yoshikawa",
            axes="trans",
            max_samples=50000,
            is_normalized=False,  # Use the slider value here
        )
        ws.plot(color="yoshikawa")


if __name__ == "__main__":
    unittest.main()
