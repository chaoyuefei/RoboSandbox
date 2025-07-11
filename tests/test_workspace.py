import unittest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch
from robosandbox.performance.workspace.WorkSpace import WorkSpace
from robosandbox.performance.workspace.indice_manager import IndiceManager


class MockRobot:
    """Mock robot class for testing."""

    def __init__(self, qlim=None):
        self.qlim = qlim if qlim is not None else (np.array([-1, -1, -1]), np.array([1, 1, 1]))
        self._manip_values = {
            "yoshikawa": np.array([0.5, 0.7, 0.3]),
            "invcondition": np.array([0.4, 0.6, 0.8]),
            "asada": np.array([0.2, 0.3, 0.4])
        }

    def manipulability(self, joint_config, method="yoshikawa", axes="all"):
        """Mock manipulability method that returns predefined values."""
        if method in self._manip_values:
            index = hash(str(joint_config)) % len(self._manip_values[method])
            return self._manip_values[method][index]
        return 0.0

    def fkine(self, joint_config):
        """Mock forward kinematics method that returns a transformation matrix."""
        # Create a mock SE3 object with a translation vector
        mock_se3 = Mock()
        # Use joint values to create deterministic but varied output
        x = np.sum(joint_config) * 0.1
        y = np.sum(joint_config) * 0.2
        z = np.sum(joint_config) * 0.3
        mock_se3.t = np.array([x, y, z])
        return mock_se3


class TestWorkSpace(unittest.TestCase):
    """Test cases for the WorkSpace class."""

    def setUp(self):
        """Set up test fixtures."""
        self.robot = MockRobot()
        self.workspace = WorkSpace(self.robot)

    def test_initialization(self):
        """Test initialization of WorkSpace."""
        self.assertEqual(self.workspace.robot, self.robot)
        self.assertIsInstance(self.workspace.df, pd.DataFrame)
        self.assertIsInstance(self.workspace.indice_manager, IndiceManager)

    def test_add_indice(self):
        """Test adding a custom indice."""
        def custom_indice(workspace, joint_points):
            return np.array([0.42, 0.42, 0.42])

        self.workspace.add_indice("custom", custom_indice, description="A custom indice")

        # Check if indice is in the list
        self.assertIn("custom", self.workspace.list_indice())

    def test_local_indice(self):
        """Test computing local indice."""
        joint_points = [
            np.array([0.1, 0.2, 0.3]),
            np.array([0.4, 0.5, 0.6]),
            np.array([0.7, 0.8, 0.9])
        ]

        # Test existing indice
        result = self.workspace.local_indice("yoshikawa", joint_points=joint_points)
        self.assertIsInstance(result, np.ndarray)

        # Test error for non-existent indice
        with self.assertRaises(ValueError):
            self.workspace.local_indice("nonexistent_indice", joint_points=joint_points)

    def test_generate_joints_samples(self):
        """Test generating joint samples."""
        num_samples = 100
        samples = self.workspace.generate_joints_samples(num_samples)

        self.assertEqual(len(samples), num_samples)
        # Check if samples are within limits
        for sample in samples:
            self.assertTrue(np.all(sample >= self.robot.qlim[0]))
            self.assertTrue(np.all(sample <= self.robot.qlim[1]))

    def test_get_cartesian_points(self):
        """Test getting cartesian points from joint points."""
        joint_points = [
            np.array([0.1, 0.2, 0.3]),
            np.array([0.4, 0.5, 0.6])
        ]

        cartesian_points = self.workspace.get_cartesian_points(joint_points)

        self.assertEqual(len(cartesian_points), len(joint_points))
        for point in cartesian_points:
            self.assertEqual(point.shape, (3,))  # x, y, z coordinates

    def test_add_samples(self):
        """Test adding samples to the workspace."""
        points = [
            np.array([1.0, 2.0, 3.0]),
            np.array([4.0, 5.0, 6.0])
        ]
        metric_values = np.array([0.5, 0.7])

        self.workspace.add_samples(points, metric_values=metric_values, metric="yoshikawa")

        # Check if samples were added correctly
        self.assertEqual(len(self.workspace.df), 2)
        self.assertIn("yoshikawa", self.workspace.df.columns)
        self.assertEqual(self.workspace.df["yoshikawa"].iloc[0], 0.5)
        self.assertEqual(self.workspace.df["yoshikawa"].iloc[1], 0.7)

    def test_get_max_distance(self):
        """Test calculating maximum distance."""
        # Add some points to the workspace
        points = [
            np.array([1.0, 0.0, 0.0]),  # distance 1
            np.array([0.0, 2.0, 0.0]),  # distance 2
            np.array([0.0, 0.0, 3.0])   # distance 3
        ]
        self.workspace.add_samples(points, metric_values=np.ones(3), metric="yoshikawa")

        # Test with default origin
        max_distance = self.workspace.get_max_distance()
        self.assertEqual(max_distance, 3.0)

        # Test with custom origin
        max_distance = self.workspace.get_max_distance(origin=[1.0, 0.0, 0.0])
        # Distance from (1,0,0) to (0,0,3) is sqrt((1-0)^2 + (0-0)^2 + (0-3)^2) = sqrt(10)
        self.assertAlmostEqual(max_distance, np.sqrt(10), places=6)

    def test_reach(self):
        """Test calculating workspace reach."""
        # Add some points to the workspace
        points = [
            np.array([1.0, 2.0, 3.0]),
            np.array([4.0, 5.0, 6.0]),
            np.array([-2.0, -3.0, -4.0])
        ]
        self.workspace.add_samples(points, metric_values=np.ones(3), metric="yoshikawa")

        # Test reach for all axes
        reach_all = self.workspace.reach(axes="all")
        self.assertEqual(len(reach_all), 3)
        self.assertEqual(reach_all[0], [-2.0, 4.0])  # x range
        self.assertEqual(reach_all[1], [-3.0, 5.0])  # y range
        self.assertEqual(reach_all[2], [-4.0, 6.0])  # z range

        # Test reach for specific axes
        self.assertEqual(self.workspace.reach(axes="x"), [-2.0, 4.0])
        self.assertEqual(self.workspace.reach(axes="y"), [-3.0, 5.0])
        self.assertEqual(self.workspace.reach(axes="z"), [-4.0, 6.0])

    def test_get_volume(self):
        """Test calculating workspace volume."""
        # Add some points to the workspace
        points = [
            np.array([1.0, 0.0, 0.0]),  # distance 1
            np.array([0.0, 2.0, 0.0]),  # distance 2
            np.array([0.0, 0.0, 3.0])   # distance 3
        ]
        self.workspace.add_samples(points, metric_values=np.ones(3), metric="yoshikawa")

        # Test volume calculation with sphere method
        volume = self.workspace.get_volume(method="sphere")
        expected_volume = (4/3) * np.pi * 3**3  # Volume of sphere with radius 3
        self.assertEqual(volume, expected_volume)

    # @patch('robosandbox.performance.workspace.WorkSpace.local_indice')
    # @patch('robosandbox.performance.workspace.WorkSpace.generate_joints_samples')
    # @patch('robosandbox.performance.workspace.WorkSpace.get_cartesian_points')
    # @patch('robosandbox.performance.workspace.WorkSpace._calc_global_indice')
    # def test_global_indice(self, mock_calc_global, mock_get_cartesian, mock_generate_samples, mock_local_indice):
    #     """Test global indice calculation with mocks."""
    #     # Configure mocks
    #     mock_generate_samples.return_value = [np.array([0.1, 0.2, 0.3])]
    #     mock_get_cartesian.return_value = [np.array([1.0, 2.0, 3.0])]
    #     mock_local_indice.return_value = np.array([0.5])
    #     mock_calc_global.return_value = 0.5

    #     # Call the method
    #     result = self.workspace.global_indice(
    #         initial_samples=10,
    #         method="yoshikawa",
    #         is_normalized=False
    #     )

    #     # Verify the result
    #     self.assertEqual(result, 0.5)

    #     # Verify mock calls
    #     mock_generate_samples.assert_called()
    #     mock_get_cartesian.assert_called()
    #     mock_local_indice.assert_called()
    #     mock_calc_global.assert_called()

    def test_list_indice(self):
        """Test listing available indices."""
        indices = self.workspace.list_indice()
        self.assertIsInstance(indices, list)
        self.assertIn("yoshikawa", indices)
        self.assertIn("invcondition", indices)
        self.assertIn("asada", indices)

    def test_calc_global_indice(self):
        """Test the internal global indice calculation method."""
        # Add some points with metrics to the workspace
        points = [
            np.array([1.0, 2.0, 3.0]),
            np.array([4.0, 5.0, 6.0])
        ]
        metric_values = np.array([0.5, 0.7])
        self.workspace.add_samples(points, metric_values=metric_values, metric="yoshikawa")

        # Test non-normalized calculation
        g_non_normalized = self.workspace._calc_global_indice(method="yoshikawa", is_normalized=False)
        self.assertEqual(g_non_normalized, 0.6)  # (0.5 + 0.7) / 2

        # Test normalized calculation
        g_normalized = self.workspace._calc_global_indice(method="yoshikawa", is_normalized=True)
        self.assertEqual(g_normalized, 0.6 / 0.7)  # (0.5 + 0.7) / (2 * 0.7)


if __name__ == "__main__":
    unittest.main()
