#!/usr/bin/env python

import numpy as np

try:
    from .Generic import GenericDH
except ImportError:
    from Generic import GenericDH


class GenericFour(GenericDH):
    """4-DOF generic robot with default DH parameters"""

    def __init__(self):
        # Default DH parameters for a 4-DOF robot
        a = [0, -0.4, -0.4, -0.4]
        d = [0.4, 0, 0, 0]
        alpha = [np.pi / 2, 0, 0, 0]

        super().__init__(dofs=4, a=a, d=d, alpha=alpha, name="GenericFour")

        # Override default ready configuration
        self.qr = np.array([0, -0.8, 0.8, 0.8])
        self.addconfiguration("qr", self.qr)

    def teach(self, realtime=True, config="qr"):
        """
        Launch an interactive teaching interface for the robot using Swift

        This method creates a Swift environment with sliders to control each
        joint of the robot in real-time. Similar to the MATLAB Robotics
        Toolbox teach() function.

        Parameters:
        -----------
        realtime : bool, optional
            Whether to run the simulation in real-time (default: True)
        config : str, optional
            Initial configuration to use ('qr', 'qz', or None for current)
            (default: 'qr')

        Returns:
        --------
        None

        Example:
        --------
        >>> robot = GenericDH(dofs=4, name="MyRobot")
        >>> robot.teach()  # Opens interactive interface with ready pose
        >>> robot.teach(config='qz')  # Start from zero configuration
        """
        try:
            import swift
            import time
        except ImportError:
            raise ImportError(
                "Swift package is required for teach functionality. "
                "Please install it with: pip install swift-sim"
            )

        # Launch the simulator Swift
        env = swift.Swift()
        env.launch(realtime=realtime)

        # Set robot to specified initial configuration
        if config == "qr":
            self.q = self.qr
        elif config == "qz":
            self.q = self.qz
        elif config is not None:
            print(f"Warning: Unknown configuration '{config}', using current pose")

        env.add(self)

        # Callback function for sliders to set joint angles
        def set_joint(j, value):
            self.q[j] = np.deg2rad(float(value))

        # Add sliders for each joint
        j = 0
        for link in self.links:
            if link.isjoint and hasattr(link, "qlim") and link.qlim is not None:
                # Add slider with joint limits and current position
                env.add(
                    swift.Slider(
                        lambda x, j=j: set_joint(j, x),
                        min=np.round(np.rad2deg(link.qlim[0]), 2),
                        max=np.round(np.rad2deg(link.qlim[1]), 2),
                        step=1,
                        value=np.round(np.rad2deg(self.q[j]), 2),
                        desc=f"{self.name} Joint {j}",
                        unit="&#176;",  # HTML unicode for degree sign
                    )
                )
                j += 1

        print(f"Teaching interface launched for {self.name}")
        print(f"Robot has {self.n} joints with the following limits:")
        j = 0
        for link in self.links:
            if link.isjoint and hasattr(link, "qlim") and link.qlim is not None:
                print(
                    f"  Joint {j}: [{np.rad2deg(link.qlim[0]):.1f}°, {np.rad2deg(link.qlim[1]):.1f}°]"
                )
                j += 1
        print(
            "Use the sliders to control joint angles. Press Ctrl+C or close the Swift window to exit."
        )

        # Main control loop
        try:
            while True:
                # Update the environment with the new robot pose
                env.step(0.0)
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("\nTeaching session ended by user.")
            print(f"Final joint configuration: {np.rad2deg(self.q)}")
        except Exception as e:
            print(f"Teaching session ended due to error: {e}")
        finally:
            # Clean up
            try:
                env.close()
            except Exception:
                pass


if __name__ == "__main__":  # pragma nocover
    from roboticstoolbox import jtraj
    import swift

    robot = GenericFour()
    q0 = robot.qz
    qe = robot.qr
    robot.teach()
