#!/usr/bin/env python
"""
@author: Chaoyue Fei
"""

from math import pi

import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH
import robosandbox.geometry.Link.CylinderLink as cl


class GenericFour(DHRobot):
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

    def __init__(self, dofs=4, links=None, alpha=[pi / 2, 0, 0, 0]):
        if links is None:
            l1 = cl(length=0.4, E=70e6, rho=2700, Rout=25e-3, parameters=[20e-3, 20e-3], method='linear')
            l2 = cl(length=0.4, E=70e6, rho=2700, Rout=25e-3, parameters=[20e-3, 20e-3], method='linear')
            l3 = cl(length=0.4, E=70e6, rho=2700, Rout=25e-3, parameters=[20e-3, 20e-3], method='linear')
            l4 = cl(length=0.4, E=70e6, rho=2700, Rout=25e-3, parameters=[20e-3, 20e-3], method='linear')
            links = [l1, l2, l3, l4]

        self.dofs = dofs
        deg = pi / 180
        d = [
            links[0].len,
            0,
            0,
            0,
        ]  # Link offset along previous z to the common normal
        a = [
            0,
            -links[1].len,
            -links[2].len,
            -links[3].len,
        ]  # Link length along common normal
        # r = [[0] * 3 for _ in range(dofs)]  # Position of COM with respect to link frame
        r = [[0, links[0].COM[-1], 0],
            [links[1].COM[-1], 0, 0],
            [links[2].COM[-1], 0, 0],
            [links[3].COM[-1], 0, 0]]
        I = [[links[0].I_tensor[0,0], links[0].I_tensor[-1,-1], links[0].I_tensor[1,1], 0, 0, 0],
            [links[1].I_tensor[-1,-1], links[1].I_tensor[0,0], links[1].I_tensor[1,1], 0, 0, 0],
            [links[2].I_tensor[-1,-1], links[2].I_tensor[0,0], links[2].I_tensor[1,1], 0, 0, 0],
            [links[3].I_tensor[-1,-1], links[3].I_tensor[0,0], links[3].I_tensor[1,1], 0, 0, 0],
        ]

        m = [links[0].mass, links[1].mass, links[2].mass, links[3].mass]  # mass of link
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
