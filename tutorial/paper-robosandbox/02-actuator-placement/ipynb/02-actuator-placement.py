import marimo

__generated_with = "0.11.30"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import robosandbox.models.DH.Generic as generic
    from robosandbox.performance.workspace import WorkSpace
    from robosandbox.optimization.sweeper import ParameterSweeper
    import plotly.graph_objects as go
    # import plotly.express as px
    import numpy as np
    return ParameterSweeper, WorkSpace, generic, go, np


@app.cell
def _(go):
    def plot_global_index_results(
        alpha_list_deg3,
        alpha_list_deg4,
        res_mat,
        plot_type="heatmap",
        method="invcondition",
        axes="all",
        isSave=False,
        step=15,
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
                    x=alpha_list_deg3,
                    y=alpha_list_deg4,
                    # colorscale='Viridis',
                    colorbar=dict(
                        title=dict(
                            text=method,
                            font=dict(size=fontsize)
                        ),
                        tickfont=dict(size=fontsize)
                    ),
                )
            )
            # Apply layout settings for heatmap
            fig.update_layout(
                xaxis_title="alpha3 (deg)",
                yaxis_title="alpha4 (deg)",
                autosize=True,
                height=800,
                width=1000,
                xaxis_title_font=dict(size=fontsize),
                yaxis_title_font=dict(size=fontsize),
                xaxis=dict(tickfont=dict(size=fontsize), dtick=step),
                yaxis=dict(tickfont=dict(size=fontsize), dtick=step),
            )
        elif plot_type == "surface":
            fontsize = 40
            fig = go.Figure(
                data=go.Surface(
                    z=G_mat,
                    x=alpha_list_deg3,
                    y=alpha_list_deg4,
                    colorbar=dict(
                        title=dict(
                            text=method,
                            font=dict(size=fontsize)
                        ),
                        tickfont=dict(size=fontsize)
                    ),
                )
            )
            # Apply proper 3D scene layout settings for surface plot
            fontsize = 16
            fig.update_layout(
                scene=dict(
                    xaxis_title="alpha3 (deg)",
                    yaxis_title="alpha4 (deg)",
                    xaxis_title_font=dict(size=40),
                    yaxis_title_font=dict(size=40),
                    # zaxis_title=method,
                    xaxis=dict(
                        tickfont=dict(size=fontsize),
                        dtick=step*4
                    ),
                    yaxis=dict(
                        # titlefont=dict(size=fontsize),
                        tickfont=dict(size=fontsize),
                        dtick=step*4
                    ),
                    zaxis=dict(
                        # titlefont=dict(size=fontsize),
                        tickfont=dict(size=fontsize)
                    ),
                    camera=dict(
                        eye=dict(x=1.5, y=1.5, z=1.5),
                        up=dict(x=0, y=0, z=1)
                    ),
                    aspectratio=dict(x=1, y=1, z=0.8)
                ),
                autosize=True,
                height=800,
                width=1000
            )
        else:
            fig = go.Figure()  # Default empty figure if plot_type is not recognized

        # Save the figure if requested
        if isSave:
            import os
            os.makedirs("fig/two_alpha", exist_ok=True)
            fig.write_image(f"fig/two_alpha/{method}_{axes}_{plot_type}.png")
            fig.write_html(f"fig/two_alpha/{method}_{axes}_{plot_type}.html")

        # Display the figure
        fig.show()

        return fig
    return (plot_global_index_results,)


@app.cell
def _(WorkSpace, generic, np):
    def obj(alpha3, alpha4, method="invcondition", axes="all", **kwargs):
        """Objective function to evaluate robot performance for given alpha values"""
        robot = generic.GenericFour(
            alpha=[np.pi / 2, alpha3, alpha4, 0]
        )
        ws = WorkSpace(robot=robot)
        G = ws.global_indice(
            initial_samples=3000,
            batch_ratio=0.1,
            error_tolerance_percentage=1e-3,
            method=method,
            axes=axes,
            max_samples=30000,
            is_normalized=kwargs.get("is_normalized", False),
        )
        return G
    return (obj,)


@app.cell
def _(mo):
    mo.md(r"""## Sweep Parameters""")
    return


@app.cell
def _(ParameterSweeper, np, obj):
    np.random.seed(42)
    # Create parameter sweeper
    sweeper = ParameterSweeper(
        objective_function=obj
    )

    # Define parameter ranges
    step = 90
    alpha3_list = np.deg2rad(np.arange(0, 181, step))
    alpha4_list = np.deg2rad(np.arange(0, 181, step))

    # Define the method and axes for the sweep
    method = "invcondition"
    axes = "all"
    filename = f"data/two_alpha/{method}_{axes}.npz"

    # Run the sweep
    # if file exists, load the results
    try:
        data = np.load(filename)
        results = data["results"]
        result_matrix = data["result_matrix"]
    except FileNotFoundError:
        # If file does not exist, perform the sweep
        results, result_matrix = sweeper.sweep(
            param_dict={"alpha3": alpha3_list, "alpha4": alpha4_list},
            fixed_params={"method": method, "axes": axes, "is_normalized": False},
            save_intermediate=False,
            save_path=filename,
        )
    return (
        alpha3_list,
        alpha4_list,
        axes,
        data,
        filename,
        method,
        result_matrix,
        results,
        step,
        sweeper,
    )


@app.cell
def _(
    alpha3_list,
    alpha4_list,
    np,
    plot_global_index_results,
    result_matrix,
    step,
):
    plot_global_index_results(
        alpha_list_deg3=alpha3_list * 180 / np.pi,
        alpha_list_deg4=alpha4_list * 180 / np.pi,
        res_mat=result_matrix,
        plot_type="heatmap",
        method="invcondition",
        axes="all",
        isSave=True,
        step=step,
    )
    return


if __name__ == "__main__":
    app.run()
