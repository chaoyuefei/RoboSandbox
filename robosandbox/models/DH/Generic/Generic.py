#!/usr/bin/env python
"""
@author: Chaoyue Fei
"""

from math import pi

import numpy as np
from roboticstoolbox import DHRobot, RevoluteDH
from robosandbox.visualization.plotly_robot import PlotlyRobot


class Generic(DHRobot, PlotlyRobot):
    """
    A fully generic robotic arm class using Denavit-Hartenberg parameters.

    The class represents a robot arm with arbitrary number of joints and fully configurable
    DH parameters. It inherits from DHRobot and uses standard DH parameters to define the kinematics.

    The robot has the following key features:
    - Configurable number of DOFs (degrees of freedom)
    - Fully customizable DH parameters: a, d, alpha, offset
    - All revolute joints with configurable joint limits
    - Ready-poses defined for:
        - qr: "ready" position (all joints at offset values)
        - qz: "zero" position (all joints at 0)
    """

    def __init__(
        self,
        dofs,
        a=None,
        d=None,
        alpha=None,
        offset=None,
        qlim=None,
        name="GenericDH",
    ):
        """
        Initialize the generic robot with configurable DH parameters.

        Args:
            dofs (int): Number of degrees of freedom
            a (list): Link lengths along common normal [dofs elements]
            d (list): Link offsets along previous z to common normal [dofs elements]
            alpha (list): Link twist angles [dofs elements]
            offset (list): Joint angle offsets [dofs elements]
            qlim (list): Joint limits as [[min, max], ...] [dofs pairs]
            name (str): Name of the robot
        """
        self.dofs = dofs
        deg = pi / 180

        # Set default values if parameters are not provided
        if a is None:
            a = [0.1] * dofs  # Default link length of 0.1m
        if d is None:
            d = [0.1] * dofs  # Default link offset of 0.1m
        if alpha is None:
            alpha = [0] * dofs  # Default twist angle of 0
        if offset is None:
            offset = [0] * dofs  # Default joint offset of 0
        if qlim is None:
            qlim = [[-180 * deg, 180 * deg]] * dofs  # Default ±180 degrees

        # Validate input dimensions
        if (
            len(a) != dofs
            or len(d) != dofs
            or len(alpha) != dofs
            or len(offset) != dofs
        ):
            raise ValueError("All DH parameter lists must have length equal to dofs")
        if len(qlim) != dofs:
            raise ValueError("qlim must have length equal to dofs")

        # Default dynamic properties (can be customized later)
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
            for i in range(dofs)
        ]

        super().__init__(
            links,
            name=name,
            keywords=("dynamics", "symbolic", "mesh"),
            manufacturer="generic",
        )

        # Ready pose: joint angles at offset values [rad]
        self.qr = np.array(offset)

        # Zero pose: joint angles [rad]
        self.qz = np.zeros(dofs)

        self.addconfiguration("qr", self.qr)
        self.addconfiguration("qz", self.qz)

    def set_dynamic_properties(
        self, m=None, r=None, I=None, Jm=None, G=None, B=None, Tc=None
    ):
        """
        Set dynamic properties for the robot links.

        Args:
            m (list): Mass of each link [dofs elements]
            r (list): Position of COM with respect to link frame [dofs x 3]
            I (list): Inertia tensor of each link [dofs x 6]
            Jm (list): Actuator inertia [dofs elements]
            G (list): Gear ratio [dofs elements]
            B (list): Viscous friction coefficient [dofs elements]
            Tc (list): Coulomb friction coefficient [dofs x 2]
        """
        if m is not None and len(m) == self.dofs:
            for i, link in enumerate(self.links):
                link.m = m[i]

        if r is not None and len(r) == self.dofs:
            for i, link in enumerate(self.links):
                link.r = r[i]

        if I is not None and len(I) == self.dofs:
            for i, link in enumerate(self.links):
                link.I = I[i]

        if Jm is not None and len(Jm) == self.dofs:
            for i, link in enumerate(self.links):
                link.Jm = Jm[i]

        if G is not None and len(G) == self.dofs:
            for i, link in enumerate(self.links):
                link.G = G[i]

        if B is not None and len(B) == self.dofs:
            for i, link in enumerate(self.links):
                link.B = B[i]

        if Tc is not None and len(Tc) == self.dofs:
            for i, link in enumerate(self.links):
                link.Tc = Tc[i]


if __name__ == "__main__":
    robot = Generic(
        dofs=4,
        a=[0, -0.5, -0.5, -0.5],
        d=[0.5, 0, 0, 0],
        alpha=[pi / 2, 0, 0, 0],
        # offset=[0, pi / 4, -pi / 4, pi / 2],
        qlim=[[-pi, pi], [-pi / 2, pi / 2], [-pi / 3, pi / 3], [-pi / 6, pi / 6]],
        name="GenericRobot",
    )
    robot.plotly(robot.qz)
