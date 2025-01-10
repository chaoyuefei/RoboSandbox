import robosandbox as rsb


def test_GenericFour():
    robot = rsb.models.DH.Generic.GenericFour()
    # robot.plot(robot.qz, block=True)
    assert robot is not None, "GenericFour robot not defined"
    assert robot.n == 4, "GenericFour robot has 4 joints"


def test_GenericThree():
    robot = rsb.models.DH.Generic.GenericThree()
    # robot.plot(robot.qz, block=True)
    assert robot is not None, "GenericThree robot not defined"
    assert robot.n == 3, "GenericThree robot has 3 joints"


def test_GenericTwo():
    robot = rsb.models.DH.Generic.GenericTwo()
    # robot.plot(robot.qz, block=True)
    assert robot is not None, "GenericTwo robot not defined"
    assert robot.n == 2, "GenericTwo robot has 2 joints"


def test_Pand():
    robot = rsb.models.DH.Panda()
    # robot.plot(robot.qz, block=True)
    assert robot is not None, "Panda robot not defined"
    assert robot.n == 7, "Panda robot has 7 joints"


# if __name__ == "__main__":
#     test_GenericFour()
