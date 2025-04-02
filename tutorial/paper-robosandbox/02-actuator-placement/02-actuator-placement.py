import marimo

__generated_with = "0.11.30"
app = marimo.App(width="medium")


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
def _():
    import marimo as mo
    return (mo,)


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
                        title=f"{method}", tickfont=dict(size=40)
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
                        title=f"{method}", tickfont=dict(size=40)
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
    return (plot_global_index_results,)


@app.cell
def _(WorkSpace, generic, np):
    def obj(alpha3, alpha4, method="invcondition", axes="all"):
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
            is_normalized=False,
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
        objective_function=obj,
        save_path=None,
    )

    # Define parameter ranges
    alpha3_list = np.linspace(0, np.pi, 13)
    alpha4_list = np.linspace(0, np.pi, 13)

    # Run the sweep
    results, result_matrix = sweeper.sweep(
        param_dict={"alpha3": alpha3_list, "alpha4": alpha4_list},
        fixed_params={"method": "invcondition", "axes": "all"},
        save_intermediate=False,
    )

    return alpha3_list, alpha4_list, result_matrix, results, sweeper


if __name__ == "__main__":
    app.run()
