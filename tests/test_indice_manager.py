import unittest
import numpy as np
from robosandbox.performance.workspace.indice_manager import IndiceManager, IndiceRegistry
from robosandbox.performance.workspace.WorkSpace import WorkSpace
import robosandbox as rsb


class TestIndiceManager(unittest.TestCase):
    def setUp(self):
        # Initialize a robot model
        self.robot = rsb.models.DH.Generic.GenericSeven()
        # Create a workspace with the robot
        self.workspace = WorkSpace(self.robot)
        # Generate some joint samples
        self.joint_points = self.workspace.generate_joints_samples(10)

    def test_standard_indices(self):
        """Test the standard indices that are available in the IndiceRegistry."""
        indice_manager = IndiceManager()
        
        # Test listing all indices
        indices = indice_manager.list_indices()
        self.assertIn("yoshikawa", indices)
        self.assertIn("invcondition", indices)
        self.assertIn("asada", indices)
        
        # Test getting indice info
        info = indice_manager.get_indices_info()
        self.assertIn("yoshikawa", info)
        self.assertTrue(isinstance(info["yoshikawa"], str))
        
        # Test calculating a standard indice
        yosh_value = indice_manager.calculate("yoshikawa", self.workspace, self.joint_points)
        self.assertTrue(isinstance(yosh_value, float))
        
        # Test retrieving a standard indice function
        func, args, kwargs, desc = indice_manager.get_indice("yoshikawa")
        self.assertTrue(callable(func))
        self.assertEqual(args, ())
        self.assertEqual(kwargs, {})
        self.assertTrue(isinstance(desc, str))

    def test_add_custom_indice(self):
        """Test adding a custom indice to the IndiceRegistry."""
        def custom_indice(workspace, joint_points, weight=1.0):
            """A custom indice that returns the average joint position."""
            joint_array = np.array(joint_points)
            return float(np.mean(joint_array) * weight)
        
        indice_manager = IndiceManager()
        
        # Add custom indice
        indice_manager.add_indice(
            name="custom_avg", 
            function=custom_indice, 
            description="Custom average joint position"
        )
        
        # Verify the indice was added to the registry
        indices = indice_manager.list_indices()
        self.assertIn("custom_avg", indices)
        
        # Calculate the custom indice
        custom_value = indice_manager.calculate("custom_avg", self.workspace, self.joint_points)
        self.assertTrue(isinstance(custom_value, float))
        
        # Test with a parameter
        custom_value_weighted = indice_manager.calculate(
            "custom_avg", self.workspace, self.joint_points, weight=2.0
        )
        self.assertAlmostEqual(custom_value_weighted, custom_value * 2.0, places=5)
        
        # Verify the indice is in the registry
        self.assertIn("custom_avg", IndiceRegistry.INDICES_MAP)
        
        # Create a new indice manager and verify it can access the custom indice
        new_indice_manager = IndiceManager()
        indices = new_indice_manager.list_indices()
        self.assertIn("custom_avg", indices)
        
        # Calculate using the new manager
        new_custom_value = new_indice_manager.calculate(
            "custom_avg", self.workspace, self.joint_points
        )
        self.assertEqual(custom_value, new_custom_value)

    def test_workspace_indice_integration(self):
        """Test that the WorkSpace class correctly integrates with IndiceManager."""
        def custom_workspace_indice(workspace, joint_points, multiplier=1.0):
            """A custom indice that returns the number of joints multiplied by a factor."""
            return float(len(joint_points) * multiplier)
        
        # Add a custom indice through the workspace
        self.workspace.add_indice(
            "joint_count", 
            custom_workspace_indice, 
            description="Count of joints multiplied by a factor"
        )
        
        # List available indices
        indices = self.workspace.list_indice()
        self.assertIn("joint_count", indices)
        
        # Calculate the indice through workspace
        result = self.workspace.indice("joint_count", self.joint_points)
        self.assertEqual(result, len(self.joint_points))
        
        # Calculate with a parameter
        result_with_param = self.workspace.indice(
            "joint_count", self.joint_points, multiplier=2.0
        )
        self.assertEqual(result_with_param, len(self.joint_points) * 2.0)
        
        # Verify that a standard indice can also be calculated
        yosh_result = self.workspace.indice("yoshikawa", self.joint_points)
        self.assertTrue(isinstance(yosh_result, float))

    def test_multiple_managers(self):
        """Test that multiple IndiceManager instances share the same registry."""
        manager1 = IndiceManager()
        manager2 = IndiceManager()
        
        # Add a custom indice to manager1
        def simple_indice(workspace, joint_points):
            return 42.0
        
        manager1.add_indice("always_42", simple_indice, description="Always returns 42")
        
        # Verify manager2 can access it
        self.assertIn("always_42", manager2.list_indices())
        
        # Calculate using manager2
        result = manager2.calculate("always_42", self.workspace, self.joint_points)
        self.assertEqual(result, 42.0)


if __name__ == "__main__":
    unittest.main()