#!/usr/bin/env python
"""
@author: Chaoyue Fei
"""

from robosandbox.models.MR.utils import *
import robosandbox.models.MR.ModernRobotics as mr

import numpy as np
import matplotlib.pyplot as plt
from robosandbox.visualization.plotly_robot import PlotlyRobot


class GenericThree(PlotlyRobot):
    def __init__(
        self,
        dofs=3,
        linklengths=[0.4] * 3,
        joint_axis_list=[
            np.array([0, 0, 1]),
            np.array([0, 1, 0]),
            np.array([0, 1, 0]),
        ],
    ):
        self.dofs = dofs
        self.linklengths = linklengths

        l1 = linklengths[0]
        l2 = linklengths[1]
        l3 = linklengths[2]

        j1 = mr.ScrewToAxis(q=np.array([0, 0, 0]), s=joint_axis_list[0], h=0)
        j2 = mr.ScrewToAxis(q=np.array([0, 0, l1]), s=joint_axis_list[1], h=0)
        j3 = mr.ScrewToAxis(q=np.array([0, 0, l1 + l2]), s=joint_axis_list[2], h=0)

        self.Slist = np.transpose(np.array([j1, j2, j3]))
        # self.M = np.array(
        #     [[0, 0, -1, 0], [-1, 0, 0, 0], [0, 1, 0, l1 + l2 + l3], [0, 0, 0, 1]]
        # )  # The home configuration (position and orientation) of the end-effector
        self.M = np.array(
            [[0, 1, 0, 0], [0, 0, -1, 0], [-1, 0, 0, l1 + l2 + l3], [0, 0, 0, 1]]
        )
        J_r1 = mr.rotation_matrix_from_vector(joint_axis_list[1])
        J_r2 = mr.rotation_matrix_from_vector(joint_axis_list[2])
        # J_r3 = mr.rotation_matrix_from_vector(joint_axis_list[])

        J1 = mr.RpToTrans(J_r1, np.array([0, 0, l1]))
        J2 = mr.RpToTrans(J_r2, np.array([0, 0, l1 + l2]))
        J3 = self.M

        self.Jlist = np.array(
            [J1, J2, J3]
        )  # List of home configuration matrices Ji for the joints

        # COM1, COM2, COM3, COM4 = (
        #     0.1441,
        #     0.1441,
        #     0.1441,
        #     0.1441,
        # )  # np.array([0, 0, 0.1441])
        # COM = np.array([COM1, COM2, COM3, COM4])
        # M01 = np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, COM[0]], [0, 0, 0, 1]])
        # M12 = np.array(
        #     [[0, 1, 0, 0], [-1, 0, 0, l1 - COM[0] + COM[1]], [0, 0, 1, 0], [0, 0, 0, 1]]
        # )
        # M23 = np.array(
        #     [
        #         [1, 0, 0, -(l2 - COM[1] + COM[2])],
        #         [0, 1, 0, 0],
        #         [0, 0, 1, 0],
        #         [0, 0, 0, 1],
        #     ]
        # )
        # M34 = np.array(
        #     [
        #         [1, 0, 0, -(l3 - COM[2] + COM[3])],
        #         [0, 1, 0, 0],
        #         [0, 0, 1, 0],
        #         [0, 0, 0, 1],
        #     ]
        # )
        # M45 = np.array(
        #     [[1, 0, 0, -(l4 - COM[3])], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        # )
        # Mlist = np.array(
        #     [M01, M12, M23, M34, M45]
        # )  # List of link frames {i} relative to {i-1} at the home position

        # J1 = np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, l1], [0, 0, 0, 1]])
        # J2 = np.array([[0, 1, 0, 0], [0, 0, -1, 0], [-1, 0, 0, l1 + l2], [0, 0, 0, 1]])
        # J3 = np.array(
        #     [[0, 1, 0, 0], [0, 0, -1, 0], [-1, 0, 0, l1 + l2 + l3], [0, 0, 0, 1]]
        # )
        # J4 = np.array(
        #     [[0, 1, 0, 0], [0, 0, -1, 0], [-1, 0, 0, l1 + l2 + l3 + l4], [0, 0, 0, 1]]
        # )

        # self.Jlist = np.array(
        #     [J1, J2, J3, J4]
        # )  # List of home configuration matrices Ji for the joints

        # m = 1.5185035229010044

        # G1 = np.diag([0.01624, 0.00046, 0.01624, m, m, m])
        # G2 = np.diag([-0.00046, 0.01624, 0.01624, m, m, m])
        # G3 = np.diag([-0.00046, 0.01624, 0.01624, m, m, m])
        # G4 = np.diag([-0.00046, 0.01624, 0.01624, m, m, m])
        # Glist = np.array(
        #     [G1, G2, G3, G4]
        # )  # Spatial inertia matrices Gi of the links, The spatial inertia matrix Gb expressed in a frame {b} at the center of mass is defined as the 6 × 6 matrix

    def fkine(self, q):
        tf = mr.FKinSpace(self.M, self.Slist, q)
        return tf

    def fkine_all(self, q):
        tfs = mr.FKinSpace_all(self.Jlist, self.Slist, q)
        return tfs

    def plot_frame(self, ax, T, arrow_length=1.0, label=None):
        """
        Plot a coordinate frame given by transformation matrix T
        """
        # Origin of the frame
        origin = T[0:3, 3]

        # Axes vectors
        x_axis = T[0:3, 0]
        y_axis = T[0:3, 1]
        z_axis = T[0:3, 2]

        # Plot the axes
        ax.quiver(
            origin[0],
            origin[1],
            origin[2],
            x_axis[0],
            x_axis[1],
            x_axis[2],
            color="#F84752",
            length=arrow_length,
            normalize=True,
        )
        ax.quiver(
            origin[0],
            origin[1],
            origin[2],
            y_axis[0],
            y_axis[1],
            y_axis[2],
            color="#BBDA55",
            length=arrow_length,
            normalize=True,
        )
        ax.quiver(
            origin[0],
            origin[1],
            origin[2],
            z_axis[0],
            z_axis[1],
            z_axis[2],
            color="#8EC1E1",
            length=arrow_length,
            normalize=True,
        )

        if label:
            ax.text(origin[0], origin[1], origin[2], label)

    def plot(self, q, arrow_length=1.0):
        """
        Plot all frames and connections between them
        """
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")

        tfs = self.fkine_all(q)

        # Plot each frame
        for i, T in enumerate(tfs):
            if i != self.dofs:
                self.plot_frame(ax, T, arrow_length=arrow_length, label=f"Joint {i}")

            # Draw lines connecting consecutive frames
            if i > 0:
                prev_origin = tfs[i - 1][0:3, 3]
                curr_origin = T[0:3, 3]
                ax.plot(
                    [prev_origin[0], curr_origin[0]],
                    [prev_origin[1], curr_origin[1]],
                    [prev_origin[2], curr_origin[2]],
                    # "k-",
                    color="#E1706E",
                    alpha=1,
                    linewidth=2,
                )

        # Set axis labels
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        # Make the plot more visually appealing
        ax.set_box_aspect([1, 1, 1])

        # Find the maximum extent in any direction
        all_points = np.vstack([T[0:3, 3] for T in tfs])
        max_range = (
            np.array(
                [all_points[:, 0].ptp(), all_points[:, 1].ptp(), all_points[:, 2].ptp()]
            ).max()
            / 2.0
        )

        mid_x = (all_points[:, 0].min() + all_points[:, 0].max()) * 0.5
        mid_y = (all_points[:, 1].min() + all_points[:, 1].max()) * 0.5
        mid_z = (all_points[:, 2].min() + all_points[:, 2].max()) * 0.5

        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)

        # plt.title("Robot Frames Visualization")
        plt.show()
