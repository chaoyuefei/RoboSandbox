import plotly.graph_objects as go


def plot_global_index_results(
    alpha_list_deg1,
    alpha_list_deg2,
    res_mat,
    plot_type="heatmap",
    method="invcondition",
    axes="all",
    isSave=False,
    step=15,
    isNormalized=False,
    colorscale='Viridis'
):
    """
    Plot the effect of alpha on the global indices using Plotly.
    """
    G_mat = res_mat
    fontsize = 40

    # Create the appropriate figure based on plot_type
    if plot_type == "heatmap":
        fig = go.Figure(
            data=go.Heatmap(
                z=G_mat,
                x=alpha_list_deg1,
                y=alpha_list_deg2,
                colorscale=colorscale,
                colorbar=dict(
                    title=dict(text=method, font=dict(size=fontsize)),
                    tickfont=dict(size=fontsize),
                ),
            )
        )
        # Apply layout settings for heatmap
        fig.update_layout(
            xaxis_title="alpha1 [deg]",
            yaxis_title="alpha2 [deg]",
            autosize=True,
            height=800,
            width=1000,
            xaxis_title_font=dict(size=fontsize),
            yaxis_title_font=dict(size=fontsize),
            xaxis=dict(tickfont=dict(size=fontsize), dtick=step*2),
            yaxis=dict(tickfont=dict(size=fontsize), dtick=step*2),
        )
    elif plot_type == "surface":
        fontsize = 40
        fig = go.Figure(
            data=go.Surface(
                z=G_mat,
                x=alpha_list_deg1,
                y=alpha_list_deg2,
                colorbar=dict(
                    title=dict(text=method, font=dict(size=fontsize)),
                    tickfont=dict(size=fontsize),
                ),
                colorscale=colorscale,
            )
        )
        # Apply proper 3D scene layout settings for surface plot
        fontsize = 17
        fig.update_layout(
            scene=dict(
                xaxis_title="alpha1 [deg]",
                yaxis_title="alpha2 [deg]",
                xaxis_title_font=dict(size=32),
                yaxis_title_font=dict(size=32),
                # zaxis_title=method,
                xaxis=dict(tickfont=dict(size=fontsize), dtick=step * 4),
                yaxis=dict(
                    # titlefont=dict(size=fontsize),
                    tickfont=dict(size=fontsize),
                    dtick=step * 4,
                ),
                # zaxis=dict(
                #     # titlefont=dict(size=fontsize),
                #     tickfont=dict(size=fontsize)
                # ),
                # Do not display z axis's tick and title
                zaxis=dict(showticklabels=False, title=""),
                camera=dict(eye=dict(x=-1.2, y=-1.2, z=1.65), up=dict(x=0, y=0, z=1)),
                # aspectratio=dict(x=1, y=1, z=0.8),
            ),
            autosize=True,
            height=800,
            width=1000,
        )
    else:
        fig = go.Figure()  # Default empty figure if plot_type is not recognized

    # Save the figure if requested
    if isSave:
        import os

        os.makedirs("fig/two_alpha", exist_ok=True)
        fig.write_image(
            f"fig/two_alpha/{method}_{axes}_{plot_type}_normalised_{isNormalized}.png"
        )
        fig.write_html(
            f"fig/two_alpha/{method}_{axes}_{plot_type}_normalised_{isNormalized}.html"
        )

    # Display the figure
    fig.show()
