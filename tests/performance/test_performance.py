import robosandbox as rsb
import pytest
from robosandbox.performance.WorkSpace import WorkSpace
import numpy as np


def test_add_samples():
    ws = WorkSpace()

    points = [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
    metric_values = [1, 2, 3]
    metric = "yoshikawa"
    ws.add_samples(points, metric_values, metric)

    assert ws.df.shape[0] == 3, "The number of samples is not correct."
    assert ws.df["x"].iloc[0] == 1, "The x value is not correct."
    assert ws.df["y"].iloc[0] == 2, "The y value is not correct."
    assert ws.df["z"].iloc[0] == 3, "The z value is not correct."
    assert ws.df["yoshikawa"].iloc[0] == 1, "The yoshikawa value is not correct."

    print(ws.df)

    points = [(10, 11, 12), (13, 14, 15)]
    metric_values = [4, 5]
    metric = "yoshikawa"
    ws.add_samples(points, metric_values, metric)

    assert ws.df.shape[0] == 5, "The number of samples is not correct."
    assert ws.df["x"].iloc[3] == 10, "The x value is not correct."
    assert ws.df["y"].iloc[3] == 11, "The y value is not correct."
    assert ws.df["z"].iloc[3] == 12, "The z value is not correct."
    assert ws.df["yoshikawa"].iloc[3] == 4, "The invcondition value is not correct."

    print(ws.df)


def test_add_metric():
    ws = WorkSpace()
    new_metric = "new_metric"
    ws.add_new_metric(new_metric)
    print(ws.metrics)
    print(len(ws.metrics))
    assert len(ws.metrics) == 4, "The number of metrics is not correct."
    assert new_metric in ws.metrics, "The new metric is not in the list of metrics."


def test_generate_joints_samples():
    robot = rsb.models.DH.Generic.GenericFour()
    ws = WorkSpace(robot)
    num_samples = 5
    qlist = ws.generate_joints_samples(num_samples)
    assert len(qlist) == num_samples, "The number of samples is not correct."
    assert len(qlist[0]) == robot.dofs, "The number of joints is not correct."

    # TODO： check qlim if works
    # qlim = robot.qlim
    # # test if the joints are within the joint limits
    # for q in qlist:
    #     assert all(qlim[i][0] <= q[i] <= qlim[i][1] for i in range(len(q))), (
    #         "The joints are not within the joint limits."
    #     )

    # print(qlist)


def test_get_cartesian_points():
    robot = rsb.models.DH.Generic.GenericFour()
    ws = WorkSpace(robot)
    num_samples = 5
    qlist = ws.generate_joints_samples(num_samples)
    cartesian_points = ws.get_cartesian_points(qlist)
    assert len(cartesian_points) == num_samples, "The number of samples is not correct."
    assert len(cartesian_points[0]) == 3, (
        "The number of cartesian points is not correct."
    )

    print(cartesian_points)


def test_calc_manipulability():
    robot = rsb.models.DH.Generic.GenericFour()
    ws = WorkSpace(robot)
    num_samples = 1
    qlist = ws.generate_joints_samples(num_samples)
    manipulability = ws.calc_manipulability(qlist, method="yoshikawa", axes="all")
    assert len(manipulability) == num_samples, (
        "The number of manipulability values is not correct"
    )
    print(manipulability)


def test_get_volume():
    robot = rsb.models.DH.Generic.GenericFour()
    ws = WorkSpace(robot)
    num_samples = 3
    qlist = ws.generate_joints_samples(num_samples)
    cartesian_points = ws.get_cartesian_points(qlist)
    ws.add_samples(cartesian_points, "yoshikawa")
    volume = ws.get_volume()
    assert volume > 0, "The volume is not correct."
    print(f"The volume is {volume}.")
    print(ws.df)
    print(ws.get_max_distance())


def test_calc_global_indice():
    robot = rsb.models.DH.Generic.GenericFour()
    ws = WorkSpace(robot)
    num_samples = 3
    qlist = ws.generate_joints_samples(num_samples)
    cartesian_points = ws.get_cartesian_points(qlist)
    mlist = ws.calc_manipulability(qlist, method="yoshikawa", axes="all")
    ws.add_samples(points=cartesian_points, metric_values=mlist, metric="yoshikawa")
    G = ws.calc_global_indice(method="yoshikawa")
    print(f"The global indice is {G}.")


def test_iter_calc_global_indice():
    robot = rsb.models.DH.Generic.GenericFour()
    ws = WorkSpace(robot)
    G = ws.iter_calc_global_indice(
        initial_samples=5000,
        batch_ratio=0.1,
        error_tolerance_percentage=1e-3,
        method="invcondition",
        axes="all",
        max_samples=50000,
    )
    print(f"The convergent global indice is {G}.")


def test_workspace_plotly():
    robot = rsb.models.DH.Generic.GenericFour()
    ws = WorkSpace(robot)
    G = ws.iter_calc_global_indice(
        initial_samples=5000,
        batch_ratio=0.1,
        error_tolerance_percentage=1e-3,
        method="invcondition",
        axes="trans",
        max_samples=50000,
    )
    # print(G)
    print(ws.df)
    ws.plot(color="invcondition")

    # print(robot.manipulability([0.3, 0.2, 0.3, 0.4], method="yoshikawa", axes="trans"))
    # print(robot.manipulability([0.2, 0.2, 0.3, 0.4], method="invcondition", axes="all"))


if __name__ == "__main__":
    # set seed
    np.random.seed(42)
    # test_add_samples()
    # test_generate_joints_samples()
    # test_get_cartesian_points()
    # test_calc_manipulability()
    # test_get_volume()
    # test_calc_global_indice()
    # test_iter_calc_global_indice()
    test_workspace_plotly()
