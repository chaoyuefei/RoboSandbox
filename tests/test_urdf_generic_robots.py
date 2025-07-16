#!/usr/bin/env python

# import unittest
# import numpy as np
# import tempfile
# import shutil
# import pathlib
# import os
# from math import pi

# # Import the classes to test
# from robosandbox.models.URDF.Generic import GenericDH
# from robosandbox.models.URDF.GenericTwo import GenericTwo
# from robosandbox.models.URDF.GenericThree import GenericThree


# class TestGenericDH(unittest.TestCase):
#     """Test suite for the GenericDH URDF-based robot class."""

#     def setUp(self):
#         """Set up test fixtures before each test method."""
#         self.test_robots = []

#     def tearDown(self):
#         """Clean up after each test method."""
#         # Clean up any generated URDF files
#         try:
#             GenericDH.cleanup_generated_urdf_files()
#         except:
#             pass

#     def test_basic_initialization(self):
#         """Test basic robot initialization with minimal parameters."""
#         robot = GenericDH(dofs=2)
#         self.test_robots.append(robot)

#         self.assertIsNotNone(robot, "GenericDH robot should be created")
#         self.assertEqual(robot.n, 2, "Robot should have 2 joints")
#         self.assertEqual(robot.name, "GenericDH", "Default name should be GenericDH")

#         # Check that URDF file was created
#         self.assertTrue(os.path.exists(robot.urdf_file_path), "URDF file should exist")

#     def test_custom_dh_parameters(self):
#         """Test robot initialization with custom DH parameters."""
#         a = [0, 0.3, 0.2]
#         d = [0.4, 0, 0]
#         alpha = [pi/2, 0, 0]
#         offset = [0, -pi/2, 0]

#         robot = GenericDH(
#             dofs=3,
#             a=a,
#             d=d,
#             alpha=alpha,
#             offset=offset,
#             name="TestRobot"
#         )
#         self.test_robots.append(robot)

#         self.assertEqual(robot.n, 3, "Robot should have 3 joints")
#         self.assertEqual(robot.name, "TestRobot", "Robot name should be TestRobot")

#         # Check stored DH parameters
#         np.testing.assert_array_equal(robot._dh_a, a, "DH parameter 'a' mismatch")
#         np.testing.assert_array_equal(robot._dh_d, d, "DH parameter 'd' mismatch")
#         np.testing.assert_array_equal(robot._dh_alpha, alpha, "DH parameter 'alpha' mismatch")
#         np.testing.assert_array_equal(robot._dh_offset, offset, "DH parameter 'offset' mismatch")

#     def test_default_parameters(self):
#         """Test that default parameters are set correctly."""
#         robot = GenericDH(dofs=3)
#         self.test_robots.append(robot)

#         # Check default DH parameters are zeros
#         np.testing.assert_array_equal(robot._dh_a, np.zeros(3), "Default 'a' should be zeros")
#         np.testing.assert_array_equal(robot._dh_d, np.zeros(3), "Default 'd' should be zeros")
#         np.testing.assert_array_equal(robot._dh_alpha, np.zeros(3), "Default 'alpha' should be zeros")
#         np.testing.assert_array_equal(robot._dh_offset, np.zeros(3), "Default 'offset' should be zeros")

#     def test_custom_joint_limits(self):
#         """Test custom joint limits."""
#         qlim = np.array([[-pi/2, -pi/3], [pi/2, pi/3]])
#         robot = GenericDH(dofs=2, qlim=qlim)
#         self.test_robots.append(robot)

#         np.testing.assert_array_equal(robot.qlim, qlim, "Joint limits should match input")

#     def test_default_joint_limits(self):
#         """Test default joint limits are ±π."""
#         robot = GenericDH(dofs=3)
#         self.test_robots.append(robot)

#         expected_qlim = np.array([[-pi, -pi, -pi], [pi, pi, pi]])
#         np.testing.assert_array_equal(robot.qlim, expected_qlim, "Default joint limits should be ±π")

#     def test_input_validation_dh_parameters(self):
#         """Test input validation for DH parameters."""
#         # Test mismatched parameter lengths
#         with self.assertRaises(ValueError):
#             GenericDH(dofs=3, a=[0.1, 0.2])  # a has wrong length

#         with self.assertRaises(ValueError):
#             GenericDH(dofs=3, d=[0.1, 0.2, 0.3, 0.4])  # d has wrong length

#         with self.assertRaises(ValueError):
#             GenericDH(dofs=3, alpha=[0, pi/2])  # alpha has wrong length

#         with self.assertRaises(ValueError):
#             GenericDH(dofs=3, offset=[0, pi/2])  # offset has wrong length

#     def test_configurations(self):
#         """Test predefined configurations."""
#         robot = GenericDH(dofs=3)
#         self.test_robots.append(robot)

#         # Test that configurations exist
#         self.assertTrue(hasattr(robot, 'qz'), "Should have qz configuration")
#         self.assertTrue(hasattr(robot, 'qr'), "Should have qr configuration")

#         # Test qz configuration (zero pose)
#         np.testing.assert_array_equal(robot.qz, np.zeros(3), "qz should be all zeros")

#         # Test qr configuration (ready pose)
#         np.testing.assert_array_equal(robot.qr, np.zeros(3), "qr should be all zeros by default")

#     def test_forward_kinematics(self):
#         """Test forward kinematics computation."""
#         robot = GenericDH(dofs=2, a=[0, 0.3], d=[0.2, 0])
#         self.test_robots.append(robot)

#         # Test forward kinematics at zero configuration
#         T = robot.fkine(robot.qz)
#         self.assertIsNotNone(T, "Forward kinematics should return a transformation matrix")

#         # Test with a different configuration
#         q_test = np.array([pi/4, pi/6])
#         T_test = robot.fkine(q_test)
#         self.assertIsNotNone(T_test, "Forward kinematics should work with any valid configuration")

#     def test_urdf_file_creation(self):
#         """Test that URDF files are created and accessible."""
#         robot1 = GenericDH(dofs=2, name="TestRobot1")
#         robot2 = GenericDH(dofs=2, name="TestRobot2")
#         self.test_robots.extend([robot1, robot2])

#         # Check that files exist
#         self.assertTrue(os.path.exists(robot1.urdf_file_path), "Robot1 URDF file should exist")
#         self.assertTrue(os.path.exists(robot2.urdf_file_path), "Robot2 URDF file should exist")

#         # Check that files are different (unique filenames)
#         self.assertNotEqual(robot1.urdf_file_path, robot2.urdf_file_path,
#                            "Different robots should have different URDF files")

#     def test_unique_filename_generation(self):
#         """Test that unique filenames are generated to avoid conflicts."""
#         robot1 = GenericDH(dofs=2, name="SameName")
#         robot2 = GenericDH(dofs=2, name="SameName")
#         self.test_robots.extend([robot1, robot2])

#         # Should generate unique filenames
#         self.assertNotEqual(robot1.urdf_file_path, robot2.urdf_file_path,
#                            "Robots with same name should get unique URDF filenames")

#     def test_urdf_file_path_property(self):
#         """Test the urdf_file_path property."""
#         robot = GenericDH(dofs=3, name="PathTest")
#         self.test_robots.append(robot)

#         path = robot.urdf_file_path
#         self.assertIsInstance(path, str, "urdf_file_path should return a string")
#         self.assertTrue(path.endswith('.urdf'), "Path should end with .urdf")
#         self.assertTrue('PathTest' in path, "Path should contain robot name")

#     def test_cleanup_generated_urdf_files(self):
#         """Test the cleanup method for generated URDF files."""
#         # Create some test robots
#         robot1 = GenericDH(dofs=2, name="CleanupTest1")
#         robot2 = GenericDH(dofs=2, name="CleanupTest2")

#         # Verify files exist
#         self.assertTrue(os.path.exists(robot1.urdf_file_path))
#         self.assertTrue(os.path.exists(robot2.urdf_file_path))

#         # Clean up all files
#         deleted_files = GenericDH.cleanup_generated_urdf_files()

#         # Verify files were deleted
#         self.assertFalse(os.path.exists(robot1.urdf_file_path))
#         self.assertFalse(os.path.exists(robot2.urdf_file_path))
#         self.assertGreater(len(deleted_files), 0, "Should have deleted some files")

#     def test_different_dof_configurations(self):
#         """Test robots with different numbers of DOFs."""
#         for dofs in [1, 2, 3, 4, 5, 6]:
#             robot = GenericDH(dofs=dofs)
#             self.test_robots.append(robot)

#             self.assertEqual(robot.n, dofs, f"Robot with {dofs} DOFs should have {dofs} joints")
#             self.assertEqual(len(robot.qz), dofs, f"qz should have {dofs} elements")
#             self.assertEqual(len(robot.qr), dofs, f"qr should have {dofs} elements")

#     def test_inheritance(self):
#         """Test that GenericDH inherits from correct base classes."""
#         robot = GenericDH(dofs=3)
#         self.test_robots.append(robot)

#         # Check inheritance from ERobot
#         from roboticstoolbox.robot.ERobot import ERobot
#         self.assertIsInstance(robot, ERobot, "Should inherit from ERobot")


# class TestGenericTwo(unittest.TestCase):
#     """Test suite for the GenericTwo robot class."""

#     def setUp(self):
#         """Set up test fixtures before each test method."""
#         self.test_robots = []

#     def tearDown(self):
#         """Clean up after each test method."""
#         try:
#             GenericDH.cleanup_generated_urdf_files()
#         except:
#             pass

#     def test_initialization(self):
#         """Test GenericTwo initialization."""
#         robot = GenericTwo()
#         self.test_robots.append(robot)

#         self.assertIsNotNone(robot, "GenericTwo robot should be created")
#         self.assertEqual(robot.n, 2, "GenericTwo should have 2 joints")
#         self.assertEqual(robot.name, "GenericTwo", "Name should be GenericTwo")

#     def test_dh_parameters(self):
#         """Test that GenericTwo has correct DH parameters."""
#         robot = GenericTwo()
#         self.test_robots.append(robot)

#         expected_a = np.array([0, 0.3])
#         expected_d = np.array([0.2, 0])
#         expected_alpha = np.array([pi/2, 0])

#         np.testing.assert_array_equal(robot._dh_a, expected_a, "DH parameter 'a' mismatch")
#         np.testing.assert_array_equal(robot._dh_d, expected_d, "DH parameter 'd' mismatch")
#         np.testing.assert_array_equal(robot._dh_alpha, expected_alpha, "DH parameter 'alpha' mismatch")

#     def test_ready_configuration(self):
#         """Test GenericTwo ready configuration."""
#         robot = GenericTwo()
#         self.test_robots.append(robot)

#         expected_qr = np.array([pi/4, pi/3])
#         np.testing.assert_array_equal(robot.qr, expected_qr, "Ready configuration mismatch")

#     def test_forward_kinematics(self):
#         """Test forward kinematics for GenericTwo."""
#         robot = GenericTwo()
#         self.test_robots.append(robot)

#         # Test at zero configuration
#         T_zero = robot.fkine(robot.qz)
#         self.assertIsNotNone(T_zero, "Forward kinematics should work at zero config")

#         # Test at ready configuration
#         T_ready = robot.fkine(robot.qr)
#         self.assertIsNotNone(T_ready, "Forward kinematics should work at ready config")

#     def test_inheritance_from_generic(self):
#         """Test that GenericTwo inherits from GenericDH."""
#         robot = GenericTwo()
#         self.test_robots.append(robot)

#         self.assertIsInstance(robot, GenericDH, "GenericTwo should inherit from GenericDH")


# class TestGenericThree(unittest.TestCase):
#     """Test suite for the GenericThree robot class."""

#     def setUp(self):
#         """Set up test fixtures before each test method."""
#         self.test_robots = []

#     def tearDown(self):
#         """Clean up after each test method."""
#         try:
#             GenericDH.cleanup_generated_urdf_files()
#         except:
#             pass

#     def test_initialization(self):
#         """Test GenericThree initialization."""
#         robot = GenericThree()
#         self.test_robots.append(robot)

#         self.assertIsNotNone(robot, "GenericThree robot should be created")
#         self.assertEqual(robot.n, 3, "GenericThree should have 3 joints")
#         self.assertEqual(robot.name, "GenericThree", "Name should be GenericThree")

#     def test_dh_parameters(self):
#         """Test that GenericThree has correct DH parameters."""
#         robot = GenericThree()
#         self.test_robots.append(robot)

#         expected_a = np.array([0, 0.3, 0.3])
#         expected_d = np.array([0.2, 0, 0])
#         expected_alpha = np.array([pi/2, 0, 0])

#         np.testing.assert_array_equal(robot._dh_a, expected_a, "DH parameter 'a' mismatch")
#         np.testing.assert_array_equal(robot._dh_d, expected_d, "DH parameter 'd' mismatch")
#         np.testing.assert_array_equal(robot._dh_alpha, expected_alpha, "DH parameter 'alpha' mismatch")

#     def test_ready_configuration(self):
#         """Test GenericThree ready configuration."""
#         robot = GenericThree()
#         self.test_robots.append(robot)

#         expected_qr = np.array([0, pi/4, -pi/2])
#         np.testing.assert_array_equal(robot.qr, expected_qr, "Ready configuration mismatch")

#     def test_forward_kinematics(self):
#         """Test forward kinematics for GenericThree."""
#         robot = GenericThree()
#         self.test_robots.append(robot)

#         # Test at zero configuration
#         T_zero = robot.fkine(robot.qz)
#         self.assertIsNotNone(T_zero, "Forward kinematics should work at zero config")

#         # Test at ready configuration
#         T_ready = robot.fkine(robot.qr)
#         self.assertIsNotNone(T_ready, "Forward kinematics should work at ready config")

#     def test_inheritance_from_generic(self):
#         """Test that GenericThree inherits from GenericDH."""
#         robot = GenericThree()
#         self.test_robots.append(robot)

#         self.assertIsInstance(robot, GenericDH, "GenericThree should inherit from GenericDH")


# class TestTeachFunctionality(unittest.TestCase):
#     """Test suite for the teach functionality (without actually launching GUI)."""

#     def setUp(self):
#         """Set up test fixtures before each test method."""
#         self.test_robots = []

#     def tearDown(self):
#         """Clean up after each test method."""
#         try:
#             GenericDH.cleanup_generated_urdf_files()
#         except:
#             pass

#     def test_teach_method_exists(self):
#         """Test that teach method exists and is callable."""
#         robot = GenericDH(dofs=2)
#         self.test_robots.append(robot)

#         self.assertTrue(hasattr(robot, 'teach'), "Robot should have teach method")
#         self.assertTrue(callable(robot.teach), "teach should be callable")

#     def test_interactive_teach_method_exists(self):
#         """Test that interactive_teach method exists and is callable."""
#         robot = GenericDH(dofs=2)
#         self.test_robots.append(robot)

#         self.assertTrue(hasattr(robot, 'interactive_teach'), "Robot should have interactive_teach method")
#         self.assertTrue(callable(robot.interactive_teach), "interactive_teach should be callable")

#     # Note: We don't test the actual teach functionality here as it requires
#     # Swift and would launch an interactive GUI, which is not suitable for automated tests


# class TestIntegration(unittest.TestCase):
#     """Integration tests for all robot classes."""

#     def setUp(self):
#         """Set up test fixtures before each test method."""
#         self.test_robots = []

#     def tearDown(self):
#         """Clean up after each test method."""
#         try:
#             GenericDH.cleanup_generated_urdf_files()
#         except:
#             pass

#     def test_all_robots_can_be_created(self):
#         """Test that all robot types can be created without errors."""
#         robots = [
#             GenericDH(dofs=2),
#             GenericDH(dofs=3, name="Custom3DOF"),
#             GenericTwo(),
#             GenericThree()
#         ]
#         self.test_robots.extend(robots)

#         for robot in robots:
#             self.assertIsNotNone(robot, f"Robot {robot.name} should be created successfully")
#             self.assertGreater(robot.n, 0, f"Robot {robot.name} should have positive DOF")

#     def test_forward_kinematics_consistency(self):
#         """Test that forward kinematics works consistently across all robot types."""
#         robots = [
#             GenericDH(dofs=2),
#             GenericTwo(),
#             GenericThree()
#         ]
#         self.test_robots.extend(robots)

#         for robot in robots:
#             # Test at zero configuration
#             T_zero = robot.fkine(robot.qz)
#             self.assertIsNotNone(T_zero, f"FK should work for {robot.name} at qz")

#             # Test at ready configuration
#             T_ready = robot.fkine(robot.qr)
#             self.assertIsNotNone(T_ready, f"FK should work for {robot.name} at qr")

#     def test_urdf_files_are_unique(self):
#         """Test that each robot gets its own URDF file."""
#         robots = [
#             GenericDH(dofs=2, name="Test1"),
#             GenericDH(dofs=3, name="Test2"),
#             GenericTwo(),
#             GenericThree()
#         ]
#         self.test_robots.extend(robots)

#         urdf_paths = [robot.urdf_file_path for robot in robots]
#         unique_paths = set(urdf_paths)

#         self.assertEqual(len(urdf_paths), len(unique_paths),
#                         "Each robot should have a unique URDF file")


# if __name__ == "__main__":
#     unittest.main()
