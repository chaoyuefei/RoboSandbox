#!/usr/bin/env python
"""
@author: Chaoyue Fei
powered by roboticstoolbox-python
"""

from math import pi

import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH
from robosandbox.visualization.plotly_robot import PlotlyRobot


class GenericSix(DHRobot, PlotlyRobot):
    """
    A generic two-link robotic arm class using Denavit-Hartenberg parameters.
    """

    def __init__(self, dofs=6, linklengths=[0.4] * 6, alpha=[pi / 2, 0, 0, 0, 0, 0]):
        self.dofs = dofs
        deg = pi / 180
        d = [
            linklengths[0],
            0,
            0,
            0,
            0,
            0,
        ]  # Link offset along previous z to the common normal
        a = [
            0,
            -linklengths[1],
            -linklengths[2],
            -linklengths[3],
            -linklengths[4],
            -linklengths[5],
        ]  # Link length along common normal
        r = [[0] * 3 for _ in range(dofs)]  # Position of COM with respect to link frame
        I = [
            [0] * 6 for _ in range(dofs)
        ]  # Inertia tensor of link with respect to COM about x,y,z axes
        m = [0] * dofs  # mass of link
        Jm = [0] * dofs  # actuator inertia
        G = [0] * dofs  # gear ratio
        B = [0] * dofs  # actuator viscous friction coefficient (measured at the motor)
        Tc = (
            [[0, 0]] * dofs
        )  # actuator Coulomb friction coefficient for direction [-,+] (measured at the motor)
        qlim = [[-180 * deg, 180 * deg]] * dofs  # minimum and maximum joint angle

        links = [
            RevoluteDH(
                d=d[i],
                a=a[i],
                alpha=alpha[i],
                r=r[i],
                I=I[i],
                m=m[i],
                Jm=Jm[i],
                G=G[i],
                B=B[i],
                Tc=Tc[i],
                qlim=qlim[i],
            )
            for i in range(dofs)
        ]

        super().__init__(
            links,
            name="GenericTwoDH",
            keywords=("dynamics", "symbolic", "mesh"),
            manufacturer="chaoyue",
        )

        # Ready pose: joint angles [rad]
        self.qr = np.array([0, -pi / 2, 0, 0, 0, 0])

        # Zero pose: joint angles [rad]
        self.qz = np.zeros(dofs)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)
