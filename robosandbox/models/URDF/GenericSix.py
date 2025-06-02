#!/usr/bin/env python

import numpy as np

try:
    from .Generic import GenericDH
except ImportError:
    from Generic import GenericDH


class GenericSix(GenericDH):
    """6-DOF generic robot with default DH parameters"""

    def __init__(self):
        # Default DH parameters for a 6-DOF robot
        a = [0, -0.4, -0.4, -0.4, -0.4, -0.4]
        d = [0.4, 0, 0, 0, 0, 0]
        alpha = [np.pi / 2, 0, 0, 0, 0, 0]

        super().__init__(dofs=6, a=a, d=d, alpha=alpha, name="GenericSix")

        # Override default ready configuration
        self.qr = np.array([0, -np.pi / 3, np.pi / 3, 0, 0, np.pi / 3])
        self.addconfiguration("qr", self.qr)


if __name__ == "__main__":  # pragma nocover
    from roboticstoolbox import jtraj
    import swift

    robot = GenericSix()
    q0 = robot.qz
    qe = robot.qr
    qtraj = jtraj(q0, qe, 100)

    env = swift.Swift()
    env.launch(realtime=True)
    env.add(robot)
    dt = 0.05

    for qk in qtraj.q:
        robot.q = qk
        env.step()
