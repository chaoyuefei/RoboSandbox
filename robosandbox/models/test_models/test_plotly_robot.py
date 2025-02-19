import numpy as np
import plotly.graph_objects as go


class PlotlyRobot:
    def __init__(self, tfs):
        self.tfs = tfs
        self.joint_positions = self.compute_joint_positions()

    def compute_joint_positions(self):
        positions = []
        for tf in self.tfs:
            position = tf[:3, 3]
            positions.append(position)
        return np.array(positions)

    def plot(self):
        fig = go.Figure()

        # Adding links between joints
        for i in range(1, len(self.joint_positions)):
            fig.add_trace(
                go.Scatter3d(
                    x=self.joint_positions[i - 1 : i + 1, 0],
                    y=self.joint_positions[i - 1 : i + 1, 1],
                    z=self.joint_positions[i - 1 : i + 1, 2],
                    mode="lines",
                    line=dict(color="#E1706E", width=16),
                    name="Link",
                )
            )

        axis_length = 0.1  # Uniform length for all axes

        # Adding axes at each joint
        for tf, pos in zip(self.tfs, self.joint_positions):
            print(pos)
            directions = ["X", "Y", "Z"]
            # colors = ["#fa8878", "#9bbf8a", "#8EC1E1"]
            colors = ["#fa8878", "#9bbf8a", "#3480b8"]

            for i in range(3):
                direction = tf[:3, i] / np.linalg.norm(tf[:3, i])
                end_point = pos + direction * axis_length

                fig.add_trace(
                    go.Scatter3d(
                        x=[pos[0], end_point[0]],
                        y=[pos[1], end_point[1]],
                        z=[pos[2], end_point[2]],
                        mode="lines",
                        line=dict(color=colors[i], width=5),
                        name=f"{directions[i]} Axis",
                    )
                )

        # Adjust the aspect ratio
        fig.update_layout(
            scene=dict(
                aspectmode="cube",
                xaxis=dict(nticks=10, range=[-1, 1]),
                yaxis=dict(nticks=10, range=[-1, 1]),
                zaxis=dict(nticks=10, range=[-1, 1]),
                xaxis_title="X",
                yaxis_title="Y",
                zaxis_title="Z",
            ),
            title="3D Robot Visualization with Joint Frames",
            width=700,
            height=700,
        )

        fig.show()


# Example transformation matrices
tfs = [
    np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]),
    np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0.4], [0, 0, 0, 1]]),
    np.array([[1, 0, 0, -0.4], [0, 0, -1, 0], [0, 1, 0, 0.4], [0, 0, 0, 1]]),
    np.array([[1, 0, 0, -0.8], [0, 0, -1, 0], [0, 1, 0, 0.4], [0, 0, 0, 1]]),
    np.array([[1, 0, 0, -1.2], [0, 0, -1, 0], [0, 1, 0, 0.4], [0, 0, 0, 1]]),
]

robot = PlotlyRobot(tfs)
robot.plot()
