import robosandbox as rsb


def test_GenericFour():
    robot = rsb.models.DHRoboLink.Generic.GenericFour()
    dyamics = robot.dynamics()
    print(robot)
    print(robot.links[-1].I)


def test_GenericFour_plot():
    robot = rsb.models.DHRoboLink.Generic.GenericFour()
    robot.plotly(robot.qr)


if __name__ == "__main__":
    test_GenericFour()
    # test_GenericFour_plot()
