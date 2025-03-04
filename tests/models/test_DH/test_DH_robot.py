import robosandbox as rsb


def test_GenericThree_define():
    robot = rsb.models.DH.Generic.GenericThree()
    # robot.plot(robot.qz, block=True)
    # robot.plotly(robot.qz)
    assert robot is not None, "GenericFour robot not defined"
    assert robot.n == 3, "GenericFour robot has 3 joints"


def test_GenericThree_plotly():
    robot = rsb.models.DH.Generic.GenericThree()
    fig = robot.plotly(robot.qr)
    assert fig is not None, "plotly return fig is not None"


if __name__ == "__main__":
    pass
    # test_GenericThree_define()
    # test_GenericThree_plotly()
