import plotly.graph_objects as go
import pandas as pd


class PlotlyWorkSpace:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def plot(
        self, color="invcondition", path="", fig=go.Figure(), isShow=True, isUpdate=True
    ):
        fig.add_trace(
            go.Scatter3d(
                x=self.df["x"],
                y=self.df["y"],
                z=self.df["z"],
                mode="markers",
                marker=dict(
                    size=5,
                    color=self.df[
                        color
                    ],  # set color to an array/list of desired values
                    # colorscale="Viridis"  # choose a colorscale
                    colorbar=dict(title=color),
                    opacity=0.5,
                ),
            )
        )
        if isUpdate:
            fig.update_layout(
                scene=dict(
                    xaxis_title="X",
                    yaxis_title="Y",
                    zaxis_title="Z",
                ),
            )
        if isShow:
            fig.show()
