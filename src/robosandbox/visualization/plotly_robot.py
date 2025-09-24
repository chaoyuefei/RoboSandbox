import numpy as np
import plotly.graph_objects as go
from typing import Optional, List, Union


class PlotlyRobot:
    def compute_joint_positions(self):
        positions = []
        for tf in self.tfs:
            if isinstance(tf, np.ndarray):
                position = tf[:3, 3]
            else:
                try:
                    position = tf.t
                except Exception as e:
                    print(f"data type is {type(tf)} and error is {e}")
            positions.append(position)
        return np.array(positions)

    def plotly(
        self,
        q,
        save=False,
        path="",
        fig=None,
        isShow=True,
        isUpdate=True,
        axis_length_factor=1.0,
        zoom_factor=1.5,
        show_z_axis: bool = True,
        show_all_axes: bool = False,
    ):
        if fig is None:
            fig = go.Figure()
        self.tfs = self.fkine_all(q)
        self.joint_positions = self.compute_joint_positions()

        # Adding links between joints
        for i in range(1, len(self.joint_positions)):
            fig.add_trace(
                go.Scatter3d(
                    x=self.joint_positions[i - 1 : i + 1, 0],
                    y=self.joint_positions[i - 1 : i + 1, 1],
                    z=self.joint_positions[i - 1 : i + 1, 2],
                    mode="lines",
                    line=dict(color="#E1706E", width=14),
                    name=f"Link{i}",
                )
            )

        # find the distance from last tf to the origin
        if isinstance(self.tfs[-1], np.ndarray):
            max_distance = np.linalg.norm(self.tfs[-1][:3, 3])
        else:
            max_distance = np.linalg.norm(self.tfs[-1].t)
        axis_length = (
            round(max_distance / 10, 2) * axis_length_factor
        )  # Uniform length for all axes
        arrow_length = axis_length / 10 * axis_length_factor  # Length of the arrowhead

        # Adding axes at each joint
        for index, (tf, pos) in enumerate(zip(self.tfs, self.joint_positions)):
            directions = ["X", "Y", "Z"]
            colors = ["#F84752", "#BBDA55", "#8EC1E1"]

            # Determine which axes to show based on parameters
            axes_to_show = []
            if show_all_axes:
                axes_to_show = [0, 1, 2]  # Show X, Y, Z axes
            elif show_z_axis:
                axes_to_show = [2]  # Show only Z axis
            else:
                continue  # Skip showing axes if both parameters are False

            for i in axes_to_show:  # only iterate over the axes we want to show
                # Determine color - special case for last frame's Z-axis
                if i == 2 and index == len(self.tfs) - 1:  # Last frame Z-axis
                    axis_color = "#800080"  # Purple for end-effector Z-axis
                else:
                    axis_color = colors[i]

                if isinstance(tf, np.ndarray):
                    direction = tf[:3, i] / np.linalg.norm(tf[:3, i])
                else:
                    try:
                        direction = tf.A[:3, i] / np.linalg.norm(tf.A[:3, i])
                    except Exception as e:
                        print(f"data type is {type(direction)} and error is {e}")
                end_point = pos + direction * axis_length

                fig.add_trace(
                    go.Scatter3d(
                        x=[pos[0], end_point[0]],
                        y=[pos[1], end_point[1]],
                        z=[pos[2], end_point[2]],
                        mode="lines",
                        line=dict(color=axis_color, width=5),
                        name=f"{directions[i]}{index} Axis",
                    )
                )

                # Add the cone (arrowhead)
                fig.add_trace(
                    go.Cone(
                        x=[end_point[0]],
                        y=[end_point[1]],
                        z=[end_point[2]],
                        u=[direction[0]],
                        v=[direction[1]],
                        w=[direction[2]],
                        sizemode="absolute",
                        sizeref=arrow_length,
                        showscale=False,
                        colorscale=[[0, axis_color], [1, axis_color]],
                        cmin=0,
                        cmax=1,
                    )
                )

        # Adjust the aspect ratio
        if isUpdate:
            fig.update_layout(
                scene=dict(
                    aspectmode="cube",
                    camera=dict(
                        eye=dict(
                            x=zoom_factor * max_distance,
                            y=-zoom_factor * max_distance,
                            z=zoom_factor * max_distance,
                        ),  # Position of the camera
                        center=dict(x=0, y=0, z=0),  # Point the camera is looking at
                        up=dict(x=0, y=0, z=1),  # Up vector direction
                    ),
                    xaxis=dict(
                        nticks=10, range=[-1.1 * max_distance, 1.1 * max_distance]
                    ),
                    yaxis=dict(
                        nticks=10, range=[-1.1 * max_distance, 1.1 * max_distance]
                    ),
                    zaxis=dict(
                        nticks=10, range=[-1.1 * max_distance, 1.1 * max_distance]
                    ),
                    xaxis_title="X",
                    yaxis_title="Y",
                    zaxis_title="Z",
                ),
                width=700,
                height=600,
            )

        if isShow:
            fig.show()
        if save:
            fig.write_image(path)
        return fig
