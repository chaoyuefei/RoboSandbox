# from roboticstoolbox.robot.PoERobot import TE0
import robosandbox as rsb
import numpy as np


def test_plot():
    robot = rsb.models.MR.Generic.GenericThree(
        joint_axis_list=[np.array([0, 0, 1]), np.array([0, 1, 0]), np.array([0, 1, 0])]
    )
    # robot.plot([0, 0, 0], scale=0.1)
    # robot.tfs = robot.fkine_all([0.1, 0.1, 0])
    # print("robot.tfs")
    # print(np.round(robot.tfs, 2))
    robot.plotly([0, 0.2, 0.1])


def test_fkine_all():
    robot = rsb.models.DH.Generic.GenericFour()
    robot.tfs = robot.fkine_all(robot.qz)
    print(robot.tfs)


if __name__ == "__main__":
    test_plot()
    # test_fkine_all()
