import unittest
import numpy as np
from math import pi
import robosandbox as rsb
from robosandbox.models.DH.Generic.Generic import Generic


class TestGenericRobot(unittest.TestCase):
    """Test suite for the Generic robot class."""

    def test_basic_initialization(self):
        """Test basic robot initialization with default parameters."""
        robot = Generic(dofs=3)
        self.assertIsNotNone(robot, "Generic robot not defined")
        self.assertEqual(robot.n, 3, "Generic robot should have 3 joints")
        self.assertEqual(robot.dofs, 3, "DOFs should be 3")
        self.assertEqual(robot.name, "GenericDH", "Default name should be GenericDH")

    def test_custom_dh_parameters(self):
        """Test robot initialization with custom DH parameters."""
        a = [0, 0.3, 0.2, 0.1]
        d = [0.4, 0, 0, 0]
        alpha = [pi / 2, 0, 0, 0]
        offset = [0, -pi / 2, 0, 0]

        robot = Generic(dofs=4, a=a, d=d, alpha=alpha, offset=offset, name="TestRobot")

        self.assertEqual(robot.n, 4, "Robot should have 4 joints")
        self.assertEqual(robot.name, "TestRobot", "Robot name should be TestRobot")

        # Check DH parameters
        for i in range(4):
            self.assertEqual(robot.links[i].a, a[i], f"Link {i} a parameter mismatch")
            self.assertEqual(robot.links[i].d, d[i], f"Link {i} d parameter mismatch")
            self.assertEqual(
                robot.links[i].alpha, alpha[i], f"Link {i} alpha parameter mismatch"
            )
            self.assertEqual(
                robot.links[i].offset, offset[i], f"Link {i} offset parameter mismatch"
            )

    def test_default_parameters(self):
        """Test that default parameters are set correctly."""
        robot = Generic(dofs=2)

        # Check default values
        for i in range(2):
            self.assertEqual(robot.links[i].a, 0.1, f"Link {i} default a should be 0.1")
            self.assertEqual(robot.links[i].d, 0.1, f"Link {i} default d should be 0.1")
            self.assertEqual(
                robot.links[i].alpha, 0, f"Link {i} default alpha should be 0"
            )
            self.assertEqual(
                robot.links[i].offset, 0, f"Link {i} default offset should be 0"
            )

    def test_custom_joint_limits(self):
        """Test custom joint limits."""
        qlim = [[-pi / 2, pi / 2], [-pi / 3, pi / 3]]
        robot = Generic(dofs=2, qlim=qlim)

        for i in range(2):
            np.testing.assert_array_almost_equal(
                robot.links[i].qlim, qlim[i], err_msg=f"Link {i} joint limits mismatch"
            )

    def test_input_validation_dh_parameters(self):
        """Test input validation for DH parameters."""
        # Test mismatched parameter lengths
        with self.assertRaises(ValueError):
            Generic(dofs=3, a=[0.1, 0.2])  # a has wrong length

        with self.assertRaises(ValueError):
            Generic(dofs=3, d=[0.1, 0.2, 0.3, 0.4])  # d has wrong length

        with self.assertRaises(ValueError):
            Generic(dofs=3, alpha=[0, pi / 2])  # alpha has wrong length

        with self.assertRaises(ValueError):
            Generic(dofs=3, offset=[0, pi / 2])  # offset has wrong length

    def test_input_validation_qlim(self):
        """Test input validation for joint limits."""
        with self.assertRaises(ValueError):
            Generic(
                dofs=3, qlim=[[-pi, pi], [-pi / 2, pi / 2]]
            )  # qlim has wrong length

    def test_configurations(self):
        """Test predefined configurations."""
        offset = [0, -pi / 2, pi / 4]
        robot = Generic(dofs=3, offset=offset)

        # Test qr configuration (ready pose at offset values)
        np.testing.assert_array_almost_equal(
            robot.qr, offset, err_msg="Ready pose should equal offset values"
        )

        # Test qz configuration (zero pose)
        np.testing.assert_array_almost_equal(
            robot.qz, np.zeros(3), err_msg="Zero pose should be all zeros"
        )

        # Test that configurations are added
        self.assertIn("qr", robot.configs, "qr configuration should be added")
        self.assertIn("qz", robot.configs, "qz configuration should be added")

    def test_forward_kinematics(self):
        """Test forward kinematics computation."""
        robot = Generic(dofs=2, a=[0, 0.3], d=[0.2, 0])

        # Test forward kinematics at zero configuration
        T = robot.fkine(robot.qz)
        self.assertIsNotNone(
            T, "Forward kinematics should return a transformation matrix"
        )
        self.assertEqual(T.shape, (4, 4), "Transformation matrix should be 4x4")

    def test_set_dynamic_properties(self):
        """Test setting dynamic properties."""
        robot = Generic(dofs=3)

        # Test setting mass
        masses = [1.0, 2.0, 1.5]
        robot.set_dynamic_properties(m=masses)
        for i, mass in enumerate(masses):
            self.assertEqual(robot.links[i].m, mass, f"Link {i} mass should be {mass}")

        # Test setting center of mass
        com_positions = [[0.1, 0, 0], [0.15, 0, 0], [0.05, 0, 0]]
        robot.set_dynamic_properties(r=com_positions)
        for i, com in enumerate(com_positions):
            np.testing.assert_array_equal(
                robot.links[i].r, com, err_msg=f"Link {i} COM position mismatch"
            )

        # Test setting actuator inertia
        inertias = [0.1, 0.15, 0.08]
        robot.set_dynamic_properties(Jm=inertias)
        for i, inertia in enumerate(inertias):
            self.assertEqual(
                robot.links[i].Jm,
                inertia,
                f"Link {i} actuator inertia should be {inertia}",
            )

    def test_different_dof_configurations(self):
        """Test robots with different numbers of DOFs."""
        for dofs in [1, 2, 3, 4, 5, 6, 7, 8]:
            robot = Generic(dofs=dofs)
            self.assertEqual(
                robot.n, dofs, f"Robot with {dofs} DOFs should have {dofs} joints"
            )
            self.assertEqual(len(robot.links), dofs, f"Robot should have {dofs} links")
            self.assertEqual(
                len(robot.qz), dofs, f"Zero pose should have {dofs} elements"
            )

    def test_inheritance(self):
        """Test that Generic inherits from correct base classes."""
        robot = Generic(dofs=3)

        # Check inheritance
        from roboticstoolbox import DHRobot
        from robosandbox.visualization.plotly_robot import PlotlyRobot

        self.assertIsInstance(robot, DHRobot, "Should inherit from DHRobot")
        self.assertIsInstance(robot, PlotlyRobot, "Should inherit from PlotlyRobot")

    def test_joint_limits_default(self):
        """Test default joint limits are ±180 degrees."""
        robot = Generic(dofs=3)
        expected_limit = [-pi, pi]

        for i in range(3):
            np.testing.assert_array_almost_equal(
                robot.links[i].qlim,
                expected_limit,
                err_msg=f"Link {i} should have default joint limits of ±180 degrees",
            )

    def test_example_from_main(self):
        """Test the example configuration from the main block."""
        robot = Generic(
            dofs=4,
            a=[0, -0.5, -0.5, -0.5],
            d=[0.5, 0, 0, 0],
            alpha=[pi / 2, 0, 0, 0],
            qlim=[[-pi, pi], [-pi / 2, pi / 2], [-pi / 3, pi / 3], [-pi / 6, pi / 6]],
            name="GenericRobot",
        )

        self.assertEqual(robot.n, 4, "Example robot should have 4 DOFs")
        self.assertEqual(
            robot.name, "GenericRobot", "Example robot name should be GenericRobot"
        )

        # Test forward kinematics works
        T = robot.fkine(robot.qz)
        self.assertIsNotNone(T, "Forward kinematics should work for example robot")

    def test_empty_dynamic_properties(self):
        """Test setting dynamic properties with None values."""
        robot = Generic(dofs=2)

        # Should not raise an error
        robot.set_dynamic_properties(m=None, r=None, I=None)

        # Values should remain at defaults (0)
        for i in range(2):
            self.assertEqual(robot.links[i].m, 0, f"Link {i} mass should remain 0")

    def test_wrong_length_dynamic_properties(self):
        """Test setting dynamic properties with wrong lengths."""
        robot = Generic(dofs=3)

        # Wrong length masses should not be applied
        wrong_masses = [1.0, 2.0]  # Only 2 elements for 3 DOF robot
        robot.set_dynamic_properties(m=wrong_masses)

        # All masses should remain 0 (default)
        for i in range(3):
            self.assertEqual(robot.links[i].m, 0, f"Link {i} mass should remain 0")


if __name__ == "__main__":
    unittest.main()
