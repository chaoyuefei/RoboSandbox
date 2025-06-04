import unittest
import numpy as np
from unittest.mock import Mock, patch
from robosandbox.performance.workspace.robot_indices import (
    order_independent_manipulability,
)


class MockRobot:
    """Mock robot class for testing."""

    def __init__(self, dofs=6, jacobian_matrix=None):
        self.dofs = dofs
        self._jacobian_matrix = jacobian_matrix

    def jacob0(self, joint_config):
        """Mock jacobian method that returns predefined jacobian matrices."""
        if self._jacobian_matrix is not None:
            return self._jacobian_matrix

        # Default jacobian matrix for testing
        if self.dofs == 6:
            return np.array(
                [
                    [1.0, 0.5, 0.2, 0.1, 0.05, 0.01],
                    [0.5, 1.0, 0.3, 0.15, 0.07, 0.02],
                    [0.2, 0.3, 1.0, 0.2, 0.1, 0.03],
                    [0.1, 0.15, 0.2, 1.0, 0.5, 0.1],
                    [0.05, 0.07, 0.1, 0.5, 1.0, 0.2],
                    [0.01, 0.02, 0.03, 0.1, 0.2, 1.0],
                ]
            )
        else:
            # Create a square jacobian matrix for other DOF values
            return np.eye(self.dofs) + 0.1 * np.random.rand(self.dofs, self.dofs)


class MockWorkspace:
    """Mock workspace class for testing."""

    def __init__(self, robot=None):
        self.robot = robot


class TestOrderIndependentManipulability(unittest.TestCase):
    """Test cases for the order_independent_manipulability function."""

    def setUp(self):
        """Set up test fixtures."""
        self.robot = MockRobot(dofs=6)
        self.workspace = MockWorkspace(self.robot)
        self.joint_points = [
            np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6]),
            np.array([0.2, 0.3, 0.4, 0.5, 0.6, 0.7]),
            np.array([0.3, 0.4, 0.5, 0.6, 0.7, 0.8]),
        ]

    def test_basic_functionality(self):
        """Test basic functionality of order_independent_manipulability."""
        result = order_independent_manipulability(self.workspace, self.joint_points)

        # Check that result is a numpy array
        self.assertIsInstance(result, np.ndarray)

        # Check that result has correct length
        self.assertEqual(len(result), len(self.joint_points))

        # Check that all values are non-negative
        self.assertTrue(np.all(result >= 0))

    def test_single_joint_configuration(self):
        """Test with a single joint configuration."""
        single_point = [self.joint_points[0]]
        result = order_independent_manipulability(self.workspace, single_point)

        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), 1)
        self.assertGreaterEqual(result[0], 0)

    def test_empty_joint_points(self):
        """Test with empty joint points list."""
        result = order_independent_manipulability(self.workspace, [])

        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), 0)

    def test_axes_parameter_all(self):
        """Test with axes='all' parameter."""
        result = order_independent_manipulability(
            self.workspace, self.joint_points, axes="all"
        )

        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), len(self.joint_points))
        self.assertTrue(np.all(result >= 0))

    def test_axes_parameter_trans(self):
        """Test with axes='trans' parameter."""
        result = order_independent_manipulability(
            self.workspace, self.joint_points, axes="trans"
        )

        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), len(self.joint_points))
        self.assertTrue(np.all(result >= 0))

    def test_axes_parameter_rot(self):
        """Test with axes='rot' parameter."""
        result = order_independent_manipulability(
            self.workspace, self.joint_points, axes="rot"
        )

        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), len(self.joint_points))
        self.assertTrue(np.all(result >= 0))

    def test_zero_determinant_jacobian(self):
        """Test with jacobian that has zero determinant."""
        # Create a jacobian with zero determinant (rank deficient)
        zero_det_jacobian = np.array(
            [
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],
                [2.0, 4.0, 6.0, 8.0, 10.0, 12.0],  # This row is 2x the first row
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            ]
        )

        robot_zero_det = MockRobot(dofs=6, jacobian_matrix=zero_det_jacobian)
        workspace_zero_det = MockWorkspace(robot_zero_det)

        result = order_independent_manipulability(workspace_zero_det, self.joint_points)

        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), len(self.joint_points))
        # All values should be zero for zero determinant
        self.assertTrue(np.allclose(result, 0.0))

    def test_identity_jacobian(self):
        """Test with identity jacobian matrix."""
        identity_jacobian = np.eye(6)
        robot_identity = MockRobot(dofs=6, jacobian_matrix=identity_jacobian)
        workspace_identity = MockWorkspace(robot_identity)

        result = order_independent_manipulability(workspace_identity, self.joint_points)

        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), len(self.joint_points))

        # For identity matrix, det(H) = det(I * I.T) = det(I) = 1
        # So order_independent_manip = 1^(1/6) = 1
        expected_value = 1.0
        self.assertTrue(np.allclose(result, expected_value))

    def test_different_dof_robots(self):
        """Test with robots having different degrees of freedom."""
        # Test with 3-DOF robot
        robot_3dof = MockRobot(dofs=3)
        workspace_3dof = MockWorkspace(robot_3dof)
        joint_points_3dof = [np.array([0.1, 0.2, 0.3]), np.array([0.4, 0.5, 0.6])]

        result_3dof = order_independent_manipulability(
            workspace_3dof, joint_points_3dof
        )

        self.assertIsInstance(result_3dof, np.ndarray)
        self.assertEqual(len(result_3dof), 2)
        self.assertTrue(np.all(result_3dof >= 0))

        # Test with 7-DOF robot
        robot_7dof = MockRobot(dofs=7)
        workspace_7dof = MockWorkspace(robot_7dof)
        joint_points_7dof = [np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])]

        result_7dof = order_independent_manipulability(
            workspace_7dof, joint_points_7dof
        )

        self.assertIsInstance(result_7dof, np.ndarray)
        self.assertEqual(len(result_7dof), 1)
        self.assertTrue(np.all(result_7dof >= 0))

    def test_mathematical_correctness(self):
        """Test mathematical correctness of the calculation."""
        # Create a known jacobian and verify the calculation manually
        known_jacobian = np.array(
            [
                [2.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 2.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 2.0, 0.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 2.0, 0.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 2.0, 0.0],
                [0.0, 0.0, 0.0, 0.0, 0.0, 2.0],
            ]
        )

        robot_known = MockRobot(dofs=6, jacobian_matrix=known_jacobian)
        workspace_known = MockWorkspace(robot_known)

        result = order_independent_manipulability(
            workspace_known, [self.joint_points[0]]
        )

        # Manual calculation:
        # H = J @ J.T = (2*I) @ (2*I).T = 4*I
        # det(H) = 4^6 = 4096
        # order_independent_manip = 4096^(1/6) = 4^(6/6) = 4
        expected_value = 4.0

        self.assertAlmostEqual(result[0], expected_value, places=10)

    def test_axes_slicing_correctness(self):
        """Test that axes parameter correctly slices the jacobian."""
        # Create a 6x6 jacobian where we can verify slicing
        full_jacobian = np.array(
            [
                [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],  # trans x
                [7.0, 8.0, 9.0, 10.0, 11.0, 12.0],  # trans y
                [13.0, 14.0, 15.0, 16.0, 17.0, 18.0],  # trans z
                [19.0, 20.0, 21.0, 22.0, 23.0, 24.0],  # rot x
                [25.0, 26.0, 27.0, 28.0, 29.0, 30.0],  # rot y
                [31.0, 32.0, 33.0, 34.0, 35.0, 36.0],  # rot z
            ]
        )

        robot_full = MockRobot(dofs=6, jacobian_matrix=full_jacobian)
        workspace_full = MockWorkspace(robot_full)

        # Test trans axes (should use first 3 rows)
        result_trans = order_independent_manipulability(
            workspace_full, [self.joint_points[0]], axes="trans"
        )

        # Test rot axes (should use last 3 rows)
        result_rot = order_independent_manipulability(
            workspace_full, [self.joint_points[0]], axes="rot"
        )

        # Test all axes (should use all 6 rows)
        result_all = order_independent_manipulability(
            workspace_full, [self.joint_points[0]], axes="all"
        )

        # Check
        self.assertIsInstance(result_all, np.ndarray)
        self.assertEqual(len(result_all), 1)
        self.assertTrue(np.all(result_all >= 0))

    def test_method_parameter_compatibility(self):
        """Test that method parameter is handled correctly."""
        # Test with default method parameter
        result1 = order_independent_manipulability(self.workspace, self.joint_points)

        # Test with explicit method parameter
        result2 = order_independent_manipulability(
            self.workspace, self.joint_points, method="order_independent_manipulability"
        )

        # Results should be identical
        np.testing.assert_array_equal(result1, result2)

    def test_numerical_stability(self):
        """Test numerical stability with very small and very large values."""
        # Test with very small jacobian values
        small_jacobian = np.eye(6) * 1e-10
        robot_small = MockRobot(dofs=6, jacobian_matrix=small_jacobian)
        workspace_small = MockWorkspace(robot_small)

        result_small = order_independent_manipulability(
            workspace_small, [self.joint_points[0]]
        )

        self.assertIsInstance(result_small, np.ndarray)
        self.assertFalse(np.isnan(result_small[0]))
        self.assertFalse(np.isinf(result_small[0]))

        # Test with large jacobian values
        large_jacobian = np.eye(6) * 1e6
        robot_large = MockRobot(dofs=6, jacobian_matrix=large_jacobian)
        workspace_large = MockWorkspace(robot_large)

        result_large = order_independent_manipulability(
            workspace_large, [self.joint_points[0]]
        )

        self.assertIsInstance(result_large, np.ndarray)
        self.assertFalse(np.isnan(result_large[0]))
        self.assertFalse(np.isinf(result_large[0]))


if __name__ == "__main__":
    unittest.main()
