# inherent from roboticstoolbox.models.UR5
#!/usr/bin/env python
import roboticstoolbox.models.URDF.UR5 as UR5Base


class UR5(UR5Base):
    """
    Class that imports a UR5 URDF model.

    This class extends the functionality of the base Panda class from the
    roboticstoolbox library, allowing for additional customizations or methods
    if needed in the future.
    """

    def __init__(self):
        super().__init__()
        # Additional initializations can be added here if necessary


if __name__ == "__main__":  # pragma nocover
    from roboticstoolbox import jtraj
    import swift
    import numpy as np
    import time

    env = swift.Swift()
    env.launch(realtime=True)

    robot = UR5()
    env.add(robot)

    # This is our callback funciton from the sliders in Swift which set
    # the joint angles of our robot to the value of the sliders
    def set_joint(j, value):
        robot.q[j] = np.deg2rad(float(value))

    # Loop through each link in the Panda and if it is a variable joint,
    # add a slider to Swift to control it
    j = 0
    for link in robot.links:
        if link.isjoint:
            # We use a lambda as the callback function from Swift
            # j=j is used to set the value of j rather than the variable j
            # We use the HTML unicode format for the degree sign in the unit arg
            env.add(
                swift.Slider(
                    lambda x, j=j: set_joint(j, x),
                    min=np.round(np.rad2deg(link.qlim[0]), 2),
                    max=np.round(np.rad2deg(link.qlim[1]), 2),
                    step=1,
                    value=np.round(np.rad2deg(robot.q[j]), 2),
                    desc="G4 Joint " + str(j),
                    unit="&#176;",
                )
            )

            j += 1

    while True:
        # Process the event queue from Swift, this invokes the callback functions
        # from the sliders if the slider value was changed
        # env.process_events()

        # Update the environment with the new robot pose
        env.step(0.0)

        time.sleep(0.01)
