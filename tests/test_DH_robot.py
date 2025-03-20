import robosandbox as rsb
import unittest

class TestRobotModels(unittest.TestCase):

    def test_GenericSeven_define(self):
        robot = rsb.models.DH.Generic.GenericSeven()
        self.assertIsNotNone(robot, "GenericSeven robot not defined")
        self.assertEqual(robot.n, 7, "GenericSeven robot should have 7 joints")

    def test_GenericSix_define(self):
        robot = rsb.models.DH.Generic.GenericSix()
        self.assertIsNotNone(robot, "GenericSix robot not defined")
        self.assertEqual(robot.n, 6, "GenericSix robot should have 6 joints")

    def test_GenericFive_define(self):
        robot = rsb.models.DH.Generic.GenericFive()
        self.assertIsNotNone(robot, "GenericFive robot not defined")
        self.assertEqual(robot.n, 5, "GenericFive robot should have 5 joints")

    def test_GenericFour_define(self):
        robot = rsb.models.DH.Generic.GenericFour()
        self.assertIsNotNone(robot, "GenericFour robot not defined")
        self.assertEqual(robot.n, 4, "GenericFour robot should have 4 joints")

    def test_GenericThree_define(self):
        robot = rsb.models.DH.Generic.GenericThree()
        self.assertIsNotNone(robot, "GenericThree robot not defined")
        self.assertEqual(robot.n, 3, "GenericThree robot should have 3 joints")

    def test_GenericTwo_define(self):
        robot = rsb.models.DH.Generic.GenericTwo()
        self.assertIsNotNone(robot, "GenericTwo robot not defined")
        self.assertEqual(robot.n, 2, "GenericTwo robot should have 2 joints")

    def test_Panda_define(self):
        robot = rsb.models.DH.Panda()
        self.assertIsNotNone(robot, "Panda robot not defined")
        self.assertEqual(robot.n, 7, "Panda robot should have 7 joints")

    def test_Puma560_define(self):
        robot = rsb.models.DH.Puma560()
        self.assertIsNotNone(robot, "Puma560 robot not defined")
        self.assertEqual(robot.n, 6, "Puma560 robot should have 6 joints")

    def test_Stanford_define(self):
        robot = rsb.models.DH.Stanford()
        self.assertIsNotNone(robot, "Stanford robot not defined")
        self.assertEqual(robot.n, 6, "Stanford robot should have 6 joints")

if __name__ == "__main__":
    unittest.main()
