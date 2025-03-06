import robosandbox as rsb


def test_GenericFour():
    robot = rsb.models.DHRoboLink.Generic.GenericFour()
    dyamics = robot.dynamics()
    print(robot)


if __name__ == "__main__":
    test_GenericFour()
