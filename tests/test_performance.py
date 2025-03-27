import robosandbox as rsb
import unittest


class TestRobotPerformance(unittest.TestCase):
    def test_workspace_define(self):
        robot = rsb.models.DH.Generic.GenericSeven()
        ws = rsb.performance.workspace.WorkSpace(robot)
        self.assertIsNotNone(ws, "WorkSpace not defined")


if __name__ == "__main__":
    unittest.main()
