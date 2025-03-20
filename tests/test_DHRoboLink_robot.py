import robosandbox as rsb
import unittest
from math import pi


class TestDHRobolink(unittest.TestCase):
    def setUp(self):
        # This method will run before each test
        self.robot = rsb.models.DHRoboLink.Generic.GenericFour()

    def test_dynamics(self):
        self.robot = rsb.models.DHRoboLink.Generic.GenericFour(
            alpha=[pi / 2, pi / 2, pi / 2, 0]
        )
        isDynamics = self.robot.hasdynamics
        offset = self.robot.offset
        self.assertEqual(
            offset, [0, 0, 0, 0], "GenericFour robot should have offset [0, 0, 0, 0]"
        )
        self.assertEqual(self.robot.n, 4, "GenericFour robot should have 4 joints")
        self.assertIsNot(
            self.robot.links[-1].I,
            [0, 0, 0, 0, 0, 0],
            "DHRoboLink robot should not have 0 inertia",
        )
        self.assertTrue(isDynamics, "GenericFour robot should have dynamics")
        self.assertFalse(
            self.robot.isspherical(), "GenericFour robot should not be spherical"
        )


if __name__ == "__main__":
    unittest.main()
