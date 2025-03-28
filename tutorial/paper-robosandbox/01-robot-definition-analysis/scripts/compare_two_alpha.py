import robosandbox as rsb
import numpy as np
import plotly.graph_objects as go
from tqdm import tqdm
import matplotlib.pyplot as plt
from robosandbox.performance.WorkSpace import WorkSpace
import plotly.express as px
import pandas as pd


def plot_global_index_results(
    alpha_list_deg3,
    alpha_list_deg4,
    res_mat,
    plot_type="heatmap",
    method="invcondition",
    axes="all",
    isSave=False,
):
    """
    Plot the effect of alpha on the global indices using Plotly.
    """
    G_mat = res_mat
    # print(G_mat)
    fig = go.Figure()
    if plot_type == "heatmap":
        fig = go.Figure(
            data=go.Heatmap(
                z=G_mat,
                x=alpha_list_deg3,
                y=alpha_list_deg4,
                # colorscale='Viridis',
                colorbar=dict(
                    title=f"{method}", titlefont=dict(size=40), tickfont=dict(size=40)
                ),
            )
        )

    if plot_type == "surface":
        fig = go.Figure(
            data=go.Surface(
                z=G_mat,
                x=alpha_list_deg3,
                y=alpha_list_deg4,
                colorbar=dict(
                    title=f"{method}", titlefont=dict(size=40), tickfont=dict(size=40)
                ),
            )
        )
        fig.update_layout(
            scene=dict(
                xaxis_title="alpha3 (deg)",
                yaxis_title="alpha4 (deg)",
                zaxis_title="",
                xaxis=dict(titlefont=dict(size=40), tickfont=dict(size=16), dtick=90),
                yaxis=dict(titlefont=dict(size=40), tickfont=dict(size=16), dtick=90),
                zaxis=dict(titlefont=dict(size=40), tickfont=dict(size=16), dtick=90),
                camera=dict(
                    eye=dict(x=1.55, y=1.55, z=1.55),
                    up=dict(x=0, y=0, z=1),
                ),
            )
        )

    fontsize = 40
    fig.update_layout(
        # title=f'Effect of alpha on global indices using {method} method and {axes} axes',
        xaxis_title="alpha3 (deg)",
        yaxis_title="alpha4 (deg)",
        autosize=True,
        height=800,
        width=1000,
        xaxis_title_font=dict(size=40),  # Font size for x-axis title
        yaxis_title_font=dict(size=40),
        xaxis=dict(tickfont=dict(size=fontsize), dtick=30),
        yaxis=dict(tickfont=dict(size=fontsize), dtick=30),
    )

    if isSave:
        fig.write_image(f"fig/two_alpha/{method}_{axes}_{plot_type}.png")
        fig.write_html(f"fig/two_alpha/{method}_{axes}_{plot_type}.html")
    fig.show()
