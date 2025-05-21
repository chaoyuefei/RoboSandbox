import robosandbox as rsb
import unittest


class TestApp(unittest.TestCase):
    # def test_plotly_Figure3D_define(self):
    #     fig = rsb.visualization.plotly_Figure3D()
    #     self.assertIsNotNone(fig, "plotly_Figure3D not defined")

    def test_app_define(self):
        app = rsb.visualization.app.RobotArmDesignApp()
        # app.run_server(debug=True)
        self.assertIsNotNone(app, "app not defined")

    # def test_app_standalone(self):
    #     app_standalone = rsb.visualization.app_standalone.RobotArmDesignAppStandalone()
    #     app_standalone.run_app()
    #     self.assertIsNotNone(app_standalone, "app_standalone not defined")


if __name__ == "__main__":
    unittest.main()
