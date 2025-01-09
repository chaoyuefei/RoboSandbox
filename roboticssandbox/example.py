import roboticstoolbox as rtb
import plotly.graph_objects as go

def define_panda():
    panda = rtb.models.Panda()
    return panda

def plot(robot, block=False):
    """
    Plot the robot in 3D

    :param robot: robot object
    :type robot: Robot subclass
    :param block: block execution until the window is closed
    :type block: bool
    """
    # Create a new figure
    fig = go.Figure()

    # Plot the robot links
    for link in robot.links:
        fig.add_trace(go.Scatter3d(
            x=link.points[:, 0],
            y=link.points[:, 1],
            z=link.points[:, 2],
            mode='lines',
            line=dict(color='blue', width=5)
        ))

    # Plot the robot joints
    for joint in robot.joints:
        fig.add_trace(go.Scatter
        (
            x=[0],
            y=[0],
            z=[0],
            mode='markers',
            marker=dict(color='red', size=10)
        ))


# # Create a Panda robot
# robot = rtb.models.Panda()

# # Display the robot
# robot.plot(block=True)
