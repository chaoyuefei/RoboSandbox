import robosandbox as rsb


def test_GenericFour():
    robot = rsb.models.DH.Generic.GenericFour()
    robot.plot(robot.qz)
    tfs = robot.fkine_all(robot.qz)
    print(tfs)
    assert robot is not None, "GenericFour robot not defined"
    assert robot.n == 4, "GenericFour robot has 4 joints"


if __name__ == "__main__":
    test_GenericFour()
