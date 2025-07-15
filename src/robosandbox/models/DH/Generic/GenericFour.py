#!/usr/bin/env python
"""
@author: Chaoyue Fei
"""

from math import pi

import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH
from robosandbox.visualization.plotly_robot import PlotlyRobot


class GenericFour(DHRobot, PlotlyRobot):
    """
    A generic four-link robotic arm class using Denavit-Hartenberg parameters.

    The class represents a four-jointed robot arm with revolute joints and specified link lengths l1-l4.
    It inherits from DHRobot and uses standard DH parameters to define the kinematics.

    The robot has the following key features:
    - 4 revolute joints with joint limits of ±180 degrees
    - Link lengths l1=0.4, l2=0.3, l3=0.2, l4=0.1 meters
    - First joint rotates around vertical axis (alpha=pi/2)
    - Other joints rotate in parallel planes (alpha=0)
    - Ready-poses defined for:
        - qr: "ready" position [0, -pi/2, 0, 0]
        - qz: "zero" position [0, 0, 0, 0]
    """

    def __init__(
        self,
        dofs=4,
        linklengths=[0.4] * 4,
        alpha=[pi / 2, 0, 0, 0],
        offset=[0, -pi / 2, 0, 0],
    ):
        self.dofs = dofs
        deg = pi / 180
        d = [
            linklengths[0],
            0,
            0,
            0,
        ]  # Link offset along previous z to the common normal
        a = [
            0,
            -linklengths[1],
            -linklengths[2],
            -linklengths[3],
        ]  # Link length along common normal
        theta = offset
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
                offset=offset[i],
                r=r[i],
                I=I[i],
                m=m[i],
                Jm=Jm[i],
                G=G[i],
                B=B[i],
                Tc=Tc[i],
                qlim=qlim[i],
            )
            for i in range(4)
        ]

        super().__init__(
            links,
            name="GenericFourDH",
            keywords=("dynamics", "symbolic", "mesh"),
            manufacturer="chaoyue",
        )

        # Ready pose: joint angles [rad]
        self.qr = np.array([0, -pi / 2, 0, 0])

        # Zero pose: joint angles [rad]
        self.qz = np.zeros(dofs)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)
