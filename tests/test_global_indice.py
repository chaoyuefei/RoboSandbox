import unittest
import robosandbox as rsb
import pandas as pd

class TestWorkSpaceGlobalIndice(unittest.TestCase):
    def test_custom_indice(self):
        # Instantiate the GenericSeven robot.
        robot = rsb.models.DH.Generic.GenericSeven()
        ws = rsb.performance.workspace.WorkSpace(robot)

        # Monkey patch methods that generate samples and compute metric values.
        ws.generate_joints_samples = lambda n: []
        ws.get_cartesian_points = lambda q: []
        ws.calc_manipulability = lambda q, method, axes: []

        # Register a custom indice function that returns a constant value.
        ws.add_indice("const", lambda ws: 42)

        # Call global_indice with the custom method "const".
        # Setting initial_samples=0 and max_samples=0 to force an immediate return.
        result = ws.global_indice(
            initial_samples=0,
            batch_ratio=0.1,
            error_tolerance_percentage=0.1,
            method="const",
            axes="all",
            max_samples=0,
            is_normalized=False
        )

        self.assertEqual(result, 42, "Custom indice function should return 42")

    def test_default_yoshikawa_indice(self):
        # Instantiate the GenericSeven robot.
        robot = rsb.models.DH.Generic.GenericSeven()
        ws = rsb.performance.workspace.WorkSpace(robot)

        # Create a sample DataFrame with default columns:
        # Columns are ["x", "y", "z", "yoshikawa", "invcondition", "asada"]
        # We set the yoshikawa values such that their average is (10+20)/2 = 15.
        sample_df = pd.DataFrame({
            "x": [0, 1],
            "y": [0, 1],
            "z": [0, 1],
            "yoshikawa": [10, 20],
            "invcondition": [None, None],
            "asada": [None, None]
        })
        ws.df = sample_df

        # Monkey patch the sampling functions to avoid modifying the already populated DataFrame.
        ws.generate_joints_samples = lambda n: []
        ws.get_cartesian_points = lambda q: []
        ws.calc_manipulability = lambda q, method, axes: []

        # Call global_indice with the default "yoshikawa" method.
        # Set max_samples equal to the current sample count to avoid iteration.
        result = ws.global_indice(
            initial_samples=0,
            batch_ratio=0.1,
            error_tolerance_percentage=0.1,
            method="yoshikawa",
            axes="all",
            max_samples=len(sample_df),
            is_normalized=False
        )

        self.assertEqual(result, 15, "Default yoshikawa indice should be 15 (average of [10, 20])")

if __name__ == '__main__':
    unittest.main()
