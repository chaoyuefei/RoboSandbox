import unittest
from robosandbox.models.DH.Generic.GenericFour import GenericFour
from robosandbox.performance.workspace import WorkSpace
import numpy as np
import plotly.graph_objects as go


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

    # def test_workspace_plot(self):
    #     robot = GenericFour(alpha=[np.pi / 2, 0, 0, 0])
    #     ws = WorkSpace(robot)
    #     G = ws.global_indice(
    #         initial_samples=3000,
    #         batch_ratio=0.1,
    #         error_tolerance_percentage=1e-2,
    #         method="yoshikawa",
    #         axes="trans",
    #         max_samples=50000,
    #         is_normalized=False,  # Use the slider value here
    #     )

    def test_isoface(self):
        robot = GenericFour(alpha=[np.pi / 2, 0, 0, 0])
        ws = WorkSpace(robot)
        G = ws.global_indice(
            initial_samples=200,
            batch_ratio=0.1,
            error_tolerance_percentage=1e-2,
            method="yoshikawa",
            axes="trans",
            max_samples=50000,
            is_normalized=False,  # Use the slider value here
        )
        print(f"len x: {len(ws.df['x'])}")
        print(f"len y: {len(ws.df['y'])}")
        print(f"len z: {len(ws.df['z'])}")
        print(f"len yoshikawa: {len(ws.df['yoshikawa'])}")

        # convert pd series to numpy arrays
        x = ws.df["x"].to_numpy()
        y = ws.df["y"].to_numpy()
        z = ws.df["z"].to_numpy()
        yoshikawa = ws.df["yoshikawa"].to_numpy()

        fig = go.Figure(
            data=go.Volume(
                x=x,
                y=y,
                z=z,
                value=yoshikawa,
                isomin=0.0,
                isomax=1.0,
            )
        )

        fig.show()


if __name__ == "__main__":
    unittest.main()
