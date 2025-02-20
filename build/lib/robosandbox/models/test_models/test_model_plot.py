import robosandbox as rsb


def test_GenericFour():
    robot = rsb.models.DH.Generic.GenericFour()
    robot.plot(robot.qz, block=True)
    # tfs = robot.fkine_all(robot.qz)
    # print(tfs)
    assert robot is not None, "GenericFour robot not defined"
    assert robot.n == 4, "GenericFour robot has 4 joints"


def test_plotly():
    robot = rsb.models.DH.Generic.GenericFour()
    # robot.plotly(robot.qr)
    robot.plotly([0, -1.57, -1, 0.5])


if __name__ == "__main__":
    # test_GenericFour()
    test_plotly()
