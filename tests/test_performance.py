import robosandbox as rsb
import unittest


class TestRobotPerformance(unittest.TestCase):
    def test_workspace_define(self):
        robot = rsb.models.DH.Generic.GenericSeven()
        ws = rsb.performance.workspace.WorkSpace(robot)
        self.assertIsNotNone(ws, "WorkSpace not defined")

    def test_workspace_global_indice(self):
        robot = rsb.models.DH.Generic.GenericFour()
        ws = rsb.performance.workspace.WorkSpace(robot)
        G = ws.global_indice(
            initial_samples=3000,
            batch_ratio=0.1,
            error_tolerance_percentage=1e-2,
            method="yoshikawa",
            axes="all",
            max_samples=50000,
            is_normalized=False,  # Use the slider value here
        )
        self.assertIsNotNone(ws, "WorkSpace not defined")
        self.assertGreaterEqual(
            len(ws.df), 3000, "WorkSpace should have at least 3000 samples"
        )
        self.assertGreater(G, 0, "Global indices should be positive")

    def test_workspace_reach(self):
        robot = rsb.models.DH.Generic.GenericFour()
        ws = rsb.performance.workspace.WorkSpace(robot)
        G = ws.global_indice(
            initial_samples=3000,
            batch_ratio=0.1,
            error_tolerance_percentage=1e-2,
            method="yoshikawa",
            axes="all",
            max_samples=50000,
            is_normalized=False,  # Use the slider value here
        )
        reach = ws.reach(axes="all")
        self.assertEqual(
            len(reach), 3, "Reach should have 3 values with x, y, z ranges"
        )
        reach_x = ws.reach(axes="x")
        self.assertEqual(
            len(reach_x), 2, "Reach should have 1 value with x range lb and ub"
        )
        reach_y = ws.reach(axes="y")
        self.assertEqual(
            len(reach_y), 2, "Reach should have 1 value with y range lb and ub"
        )
        reach_z = ws.reach(axes="z")
        self.assertEqual(
            len(reach_z), 2, "Reach should have 1 value with z range lb and ub"
        )


if __name__ == "__main__":
    unittest.main()
