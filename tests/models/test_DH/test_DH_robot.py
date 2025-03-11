import robosandbox as rsb


def test_GenericSeven_define():
    robot = rsb.models.DH.Generic.GenericSeven()
    # robot.plot(robot.qz, block=True)
    assert robot is not None, "GenericSeven robot not defined"
    assert robot.n == 7, "GenericSeven robot has 7 joints"


def test_GenericSeven_plotly():
    robot = rsb.models.DH.Generic.GenericSeven()
    fig = robot.plotly(robot.qr)
    assert fig is not None, "plotly return fig is not None"


def test_GenericSix_define():
    robot = rsb.models.DH.Generic.GenericSix()
    # robot.plot(robot.qz, block=True)
    assert robot is not None, "GenericSix robot not defined"
    assert robot.n == 6, "GenericSix robot has 6 joints"


def test_GenericSix_plotly():
    robot = rsb.models.DH.Generic.GenericSix()
    fig = robot.plotly(robot.qr)
    assert fig is not None, "plotly return fig is not None"


def test_GenericFive_define():
    robot = rsb.models.DH.Generic.GenericFive()
    # robot.plot(robot.qz, block=True)
    assert robot is not None, "GenericFive robot not defined"
    assert robot.n == 5, "GenericFive robot has 5 joints"


def test_GenericFive_plotly():
    robot = rsb.models.DH.Generic.GenericFive()
    fig = robot.plotly(robot.qr)
    assert fig is not None, "plotly return fig is not None"


def test_GenericFour_define():
    robot = rsb.models.DH.Generic.GenericFour()
    # robot.plot(robot.qz, block=True)
    assert robot is not None, "GenericFour robot not defined"
    assert robot.n == 4, "GenericFour robot has 4 joints"


def test_GenericFour_plotly():
    robot = rsb.models.DH.Generic.GenericFour()
    fig = robot.plotly(robot.qr)
    assert fig is not None, "plotly return fig is not None"


def test_GenericThree_define():
    robot = rsb.models.DH.Generic.GenericThree()
    # robot.plot(robot.qz, block=True)
    # robot.plotly(robot.qz)
    assert robot is not None, "GenericThree robot not defined"
    assert robot.n == 3, "GenericThree robot has 3 joints"


def test_GenericThree_plotly():
    robot = rsb.models.DH.Generic.GenericThree()
    fig = robot.plotly(robot.qr)
    assert fig is not None, "plotly return fig is not None"


def test_GenericTwo_define():
    robot = rsb.models.DH.Generic.GenericTwo()
    assert robot is not None, "GenericTwo robot not defined"
    assert robot.n == 2, "GenericTwo robot has 2 joints"


def test_GenericTwo_plotly():
    robot = rsb.models.DH.Generic.GenericTwo()
    fig = robot.plotly(robot.qr)
    assert fig is not None, "plotly return fig is not None"


def test_Panda_define():
    robot = rsb.models.DH.Panda()
    assert robot is not None, "Panda robot not defined"
    assert robot.n == 7, "Panda robot has 7 joints"


def test_Panda_plotly():
    robot = rsb.models.DH.Panda()
    fig = robot.plotly(robot.qr)
    assert fig is not None, "plotly return fig is not None"


def test_Panda_workspace():
    robot = rsb.models.DH.Panda()
    ws = rsb.performance.WorkSpace.WorkSpace(robot)
    # ws = WorkSpace(robot)
    G = ws.iter_calc_global_indice(
        initial_samples=5000,
        batch_ratio=0.1,
        error_tolerance_percentage=1e-3,
        method="invcondition",
        axes="all",
        max_samples=50000,
    )
    ws.plot(color="invcondition", isShow=True)


def test_Puma560_define():
    robot = rsb.models.DH.Puma560()
    assert robot is not None, "Puma560 robot not defined"
    assert robot.n == 6, "Puma560 robot has 6 joints"


def test_Puma560_plotly():
    robot = rsb.models.DH.Puma560()
    fig = robot.plotly(robot.qr)
    assert fig is not None, "plotly return fig is not None"


def test_Puma560_workspace():
    robot = rsb.models.DH.Puma560()
    ws = rsb.performance.WorkSpace.WorkSpace(robot)
    # ws = WorkSpace(robot)
    G = ws.iter_calc_global_indice(
        initial_samples=5000,
        batch_ratio=0.1,
        error_tolerance_percentage=1e-3,
        method="invcondition",
        axes="all",
        max_samples=50000,
    )
    ws.plot(color="invcondition", isShow=True)


def test_Stanford_define():
    robot = rsb.models.DH.Stanford()
    assert robot is not None, "Stanford robot not defined"
    assert robot.n == 6, "Stanford robot has 6 joints"


def test_Stanford_plotly():
    robot = rsb.models.DH.Stanford()
    fig = robot.plotly(robot.qr)
    assert fig is not None, "plotly return fig is not None"


def test_Stanford_workspace():
    robot = rsb.models.DH.Stanford()
    ws = rsb.performance.WorkSpace.WorkSpace(robot)
    # ws = WorkSpace(robot)
    G = ws.iter_calc_global_indice(
        initial_samples=5000,
        batch_ratio=0.1,
        error_tolerance_percentage=1e-3,
        method="invcondition",
        axes="all",
        max_samples=50000,
    )
    ws.plot(color="invcondition", isShow=True)


if __name__ == "__main__":
    pass
    # test_GenericThree_define()
    # test_GenericThree_plotly()
    # test_GenericTwo_define()
    # test_GenericTwo_plotly()
    # test_Panda_define()
    # test_Panda_plotly()
    # test_Panda_workspace()
    # test_Puma560_define()
    # test_Puma560_plotly()
    # test_Puma560_workspace()
    # test_Stanford_define()
    test_Stanford_plotly()
