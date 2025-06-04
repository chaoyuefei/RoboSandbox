import unittest
import numpy as np
import pandas as pd
from robosandbox.performance.workspace.indice_manager import (
    IndiceRegistry,
    IndiceManager,
)
from robosandbox.performance.workspace.robot_indices import (
    yoshikawa,
    invcondition,
    asada,
)


class MockWorkspace:
    """Mock workspace class for testing."""

    def __init__(self, robot=None):
        self.robot = robot


class MockRobot:
    """Mock robot class for testing."""

    def __init__(self, jacobian_values=None):
        self.jacobian_values = jacobian_values if jacobian_values is not None else []
        self._manip_values = {
            "yoshikawa": np.array([0.5, 0.7, 0.3]),
            "invcondition": np.array([0.4, 0.6, 0.8]),
            "asada": np.array([0.2, 0.3, 0.4]),
        }

    def manipulability(self, joint_config, method="yoshikawa", axes="all"):
        """Mock manipulability method that returns predefined values."""
        if method in self._manip_values:
            index = hash(str(joint_config)) % len(self._manip_values[method])
            return self._manip_values[method][index]
        return 0.0


class TestRobotIndices(unittest.TestCase):
    """Test cases for the robot indices functions."""

    def setUp(self):
        """Set up test fixtures."""
        self.robot = MockRobot()
        self.workspace = MockWorkspace(self.robot)
        self.joint_points = [
            np.array([0.1, 0.2, 0.3]),
            np.array([0.4, 0.5, 0.6]),
            np.array([0.7, 0.8, 0.9]),
        ]

    def test_yoshikawa(self):
        """Test the Yoshikawa index calculation."""
        result = yoshikawa(self.workspace, self.joint_points)
        self.assertIsInstance(result, np.ndarray)

    def test_invcondition(self):
        """Test the inverse condition number index calculation."""
        result = invcondition(self.workspace, self.joint_points)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), 3)

    def test_asada(self):
        """Test the Asada index calculation."""
        result = asada(self.workspace, self.joint_points)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), 3)


class TestIndiceRegistry(unittest.TestCase):
    """Test cases for the IndiceRegistry class."""

    def test_get_all_indices(self):
        """Test retrieving all indices from the registry."""
        indices = IndiceRegistry.get_all_indices()
        self.assertIsInstance(indices, dict)
        self.assertIn("yoshikawa", indices)
        self.assertIn("invcondition", indices)
        self.assertIn("asada", indices)

    def test_get_function(self):
        """Test retrieving a function by name."""
        function = IndiceRegistry.get_function("yoshikawa")
        self.assertEqual(function, yoshikawa)

        # Test error for non-existent indice
        with self.assertRaises(ValueError):
            IndiceRegistry.get_function("nonexistent_indice")

    def test_get_description(self):
        """Test retrieving a description by name."""
        description = IndiceRegistry.get_description("yoshikawa")
        self.assertIsInstance(description, str)
        self.assertIn("Yoshikawa", description)

        # Test error for non-existent indice
        with self.assertRaises(ValueError):
            IndiceRegistry.get_description("nonexistent_indice")


class TestIndiceManager(unittest.TestCase):
    """Test cases for the IndiceManager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = IndiceManager()
        self.workspace = MockWorkspace(MockRobot())
        self.joint_points = [
            np.array([0.1, 0.2, 0.3]),
            np.array([0.4, 0.5, 0.6]),
            np.array([0.7, 0.8, 0.9]),
        ]

    def test_initialization(self):
        """Test initialization of IndiceManager."""
        self.assertIsInstance(self.manager, IndiceManager)

    def test_add_custom_indice(self):
        """Test adding a custom indice."""

        # Define a custom indice function
        def custom_indice(workspace, joint_points):
            return 0.42

        # Add the custom indice
        self.manager.add_indice("custom", custom_indice, description="A custom indice")

        # Verify it was added to the registry
        self.assertIn("custom", IndiceRegistry.INDICES_MAP)
        function, description = IndiceRegistry.INDICES_MAP["custom"]
        self.assertEqual(function, custom_indice)
        self.assertEqual(description, "A custom indice")

    def test_get_indice(self):
        """Test retrieving an indice."""
        function, args, kwargs, description = self.manager.get_indice("yoshikawa")
        self.assertEqual(function, yoshikawa)
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {})
        self.assertIsInstance(description, str)

        # Test error for non-existent indice
        with self.assertRaises(ValueError):
            self.manager.get_indice("nonexistent_indice")

    def test_list_indices(self):
        """Test listing all indices."""
        indices = self.manager.list_indices()
        self.assertIsInstance(indices, list)
        self.assertIn("yoshikawa", indices)
        self.assertIn("invcondition", indices)
        self.assertIn("asada", indices)

    def test_get_indices_info(self):
        """Test getting information about all indices."""
        info = self.manager.get_indices_info()
        self.assertIsInstance(info, dict)
        self.assertIn("yoshikawa", info)
        self.assertIsInstance(info["yoshikawa"], str)

    def test_calculate(self):
        """Test calculating an indice."""
        result = self.manager.calculate("yoshikawa", self.workspace, self.joint_points)
        self.assertIsInstance(result, np.ndarray)

        # Test error for non-existent indice
        with self.assertRaises(ValueError):
            self.manager.calculate(
                "nonexistent_indice", self.workspace, self.joint_points
            )


if __name__ == "__main__":
    unittest.main()
