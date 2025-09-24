#!/usr/bin/env python
"""
@author: Chaoyue Fei
"""

from robosandbox.models.MR.utils import *
import numpy as np

# from roboticstoolbox import jtraj
import matplotlib.pyplot as plt


class GenericFour:
    def __init__(self, link_length=np.array([0.4, 0.4, 0.4, 0.4])):
        # link length
        # l1, l2, l3, l4 = 0.4, 0.4, 0.4, 0.4
        l1 = link_length[0]
        l2 = link_length[1]
        l3 = link_length[2]
        l4 = link_length[3]
        print(type(l1))
        # joints screw list

        if is_casadi_type(l1):
            j1 = ScrewToAxis(q=ca.vertcat([0, 0, 0]), s=ca.vertcat([0, 0, 1]), h=0)
        elif not is_casadi_type(l1):
            j1 = ScrewToAxis(q=np.array([0, 0, 0]), s=np.array([0, 0, 1]), h=0)
        else:
            raise ValueError(
                "Unexpected type for l1. Cannot determine how to create j1."
            )

        j2 = ScrewToAxis(q=np.array([0, 0, l1]), s=np.array([0, 1, 0]), h=0)
        j3 = ScrewToAxis(q=np.array([0, 0, l1 + l2]), s=np.array([0, 1, 0]), h=0)
        j4 = ScrewToAxis(q=np.array([0, 0, l1 + l2 + l3]), s=np.array([0, 1, 0]), h=0)
        # self.Slist = np.array([j1, j2, j3, j4]).T # Screw axes Si of the joints in a space frame, in the format
        #                                     # of a matrix with axes as the columns
        #
        print(f"j1: {j1}")
        print(f"j2: {j2}")
        print(f"j3: {j3}")
        print(f"j4: {j4}")
        self.Slist = np.transpose(np.array([j1, j2, j3, j4]))
        self.M = np.array(
            [[0, 0, -1, 0], [-1, 0, 0, 0], [0, 1, 0, l1 + l2 + l3 + l4], [0, 0, 0, 1]]
        )  # The home configuration (position and orientation) of the end-effector

        # qr = np.array([0, -np.pi / 2, 0, 0])
        # theta_list = np.array([0, 0.2, 0, 0.2])
        # theta_list = qr
        # T = mr.FKinSpace(M, Slist, theta_list)

        COM1, COM2, COM3, COM4 = (
            0.1441,
            0.1441,
            0.1441,
            0.1441,
        )  # np.array([0, 0, 0.1441])
        COM = np.array([COM1, COM2, COM3, COM4])
        M01 = np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, COM[0]], [0, 0, 0, 1]])
        M12 = np.array(
            [[0, 1, 0, 0], [-1, 0, 0, l1 - COM[0] + COM[1]], [0, 0, 1, 0], [0, 0, 0, 1]]
        )
        M23 = np.array(
            [
                [1, 0, 0, -(l2 - COM[1] + COM[2])],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )
        M34 = np.array(
            [
                [1, 0, 0, -(l3 - COM[2] + COM[3])],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )
        M45 = np.array(
            [[1, 0, 0, -(l4 - COM[3])], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        )
        Mlist = np.array(
            [M01, M12, M23, M34, M45]
        )  # List of link frames {i} relative to {i-1} at the home position

        J1 = np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, l1], [0, 0, 0, 1]])
        J2 = np.array([[0, 1, 0, 0], [0, 0, -1, 0], [-1, 0, 0, l1 + l2], [0, 0, 0, 1]])
        J3 = np.array(
            [[0, 1, 0, 0], [0, 0, -1, 0], [-1, 0, 0, l1 + l2 + l3], [0, 0, 0, 1]]
        )
        J4 = np.array(
            [[0, 1, 0, 0], [0, 0, -1, 0], [-1, 0, 0, l1 + l2 + l3 + l4], [0, 0, 0, 1]]
        )

        self.Jlist = np.array(
            [J1, J2, J3, J4]
        )  # List of home configuration matrices Ji for the joints

        m = 1.5185035229010044

        G1 = np.diag([0.01624, 0.00046, 0.01624, m, m, m])
        G2 = np.diag([-0.00046, 0.01624, 0.01624, m, m, m])
        G3 = np.diag([-0.00046, 0.01624, 0.01624, m, m, m])
        G4 = np.diag([-0.00046, 0.01624, 0.01624, m, m, m])
        Glist = np.array(
            [G1, G2, G3, G4]
        )  # Spatial inertia matrices Gi of the links, The spatial inertia matrix Gb expressed in a frame {b} at the center of mass is defined as the 6 × 6 matrix

    def fkine(self, theta_list):
        Tlist = FKinSpace(self.M, self.Slist, theta_list)

        # (self.Jlist, self.Slist, theta_list)
        return Tlist

    def plot_frame(self, ax, T, scale=1.0, label=None):
        """
        Plot a coordinate frame given by transformation matrix T
        """
        # Origin of the frame
        origin = T[0:3, 3]

        # Axes vectors
        x_axis = T[0:3, 0]
        print(f"x_axis: {x_axis}")
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
            color="r",
            length=scale,
            normalize=True,
        )
        ax.quiver(
            origin[0],
            origin[1],
            origin[2],
            y_axis[0],
            y_axis[1],
            y_axis[2],
            color="g",
            length=scale,
            normalize=True,
        )
        ax.quiver(
            origin[0],
            origin[1],
            origin[2],
            z_axis[0],
            z_axis[1],
            z_axis[2],
            color="b",
            length=scale,
            normalize=True,
        )

        if label:
            ax.text(origin[0], origin[1], origin[2], label)

    def plot_robot(self, T_list, scale=1.0):
        """
        Plot all frames and connections between them
        """
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection="3d")

        # Plot each frame
        for i, T in enumerate(T_list):
            if i != 4:
                self.plot_frame(ax, T, scale=scale, label=f"Joint {i}")

            # Draw lines connecting consecutive frames
            if i > 0:
                prev_origin = T_list[i - 1][0:3, 3]
                curr_origin = T[0:3, 3]
                ax.plot(
                    [prev_origin[0], curr_origin[0]],
                    [prev_origin[1], curr_origin[1]],
                    [prev_origin[2], curr_origin[2]],
                    "k-",
                    alpha=0.5,
                    linewidth=2,
                )

        # Set axis labels
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        # Make the plot more visually appealing
        ax.set_box_aspect([1, 1, 1])

        # Find the maximum extent in any direction
        all_points = np.vstack([T[0:3, 3] for T in T_list])
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

        plt.title("Robot Frames Visualization")
        plt.show()


# plot_robot(Tlist, scale=0.1)  # Adjust scale as needed
